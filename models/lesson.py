import enum
from api.app import db
from datetime import datetime
from flask import abort
import models.student as student_module
from models.user import User
from api.utils.utils import Updateable, get_date
from api.utils.lessonspace import create_lesson_space
from sqlalchemy.orm import joinedload


# Define a many-to-many relationship between students and lessons
student_lessons = db.Table('student_lessons',
                           db.Column('student_id', db.Integer, db.ForeignKey(
                               'student.id'), primary_key=True, index=True),
                           db.Column('lesson_id', db.Integer,
                                     db.ForeignKey('lesson.id'), primary_key=True, index=True),
                           extend_existing=True)


class LessonStatus(enum.Enum):
    """
    Enum for Lesson status.

    To add this type in migration add:
    from sqlalchemy.dialects import postgresql
    student_status = postgresql.ENUM('attended', 'scheduled', 'bad cancellation student','bad cancellation teacher','good cancellation', name='lessonstatus')
    student_status.create(op.get_bind())
    """
    ATTENDED = "attended"
    SCHEDULED = "scheduled"
    BADCANCELLATIONSTUDENT = "bad cancellation student"
    BADCANCELLATIONTEACHER = "bad cancellation teacher"
    GOODCANCELLATION = 'good cancellation'
    EXPIRED = 'expired'


class Lesson(Updateable, db.Model):
    """
    Model for Lessons.
    """

    __tablename__ = "lesson"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)

    # Many Lessons to One Teacher
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        'teacher.id'), nullable=False, index=True)

    created_at = db.Column(db.DateTime, nullable=False, default=get_date)
    last_updated = db.Column(db.DateTime, nullable=False,
                             default=get_date, onupdate=get_date)
    secret = db.Column(db.String, nullable=True)
    trial_lesson = db.Column(db.Boolean, nullable=True,
                             default=False, server_default='f')
    paid = db.Column(db.Boolean, nullable=True,
                     default=False, server_default='f')
    space_id = db.Column(db.String, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True, )
    space = db.Column(db.String, nullable=False)
    from_time = db.Column(db.DateTime, nullable=True)
    to_time = db.Column(db.DateTime, nullable=True)
    duration_in_minutes = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    completion_notes = db.Column(db.Text, nullable=True)
    wage = db.Column(db.Float, nullable=False)
    session_id = db.Column(db.String, nullable=True)
    lesson_reminder_sent_at = db.Column(db.DateTime, nullable=True)

    status = db.Column(
        db.Enum(
            LessonStatus,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=LessonStatus.SCHEDULED.value,
        server_default=LessonStatus.SCHEDULED.value,
        index=True
    )

    @property
    def get_colors(self):
        colors = {
            "attended": "#00AB55",
            "scheduled": "#FFC107",
            "expired": "#FF4842",
            "bad cancellation student": "#FF4842",
            "bad cancellation teacher": "#FF4842",
            "good cancellation": "#FF4842"
        }
        return colors

    def to_calendar(self):

        student_data = next(iter(self.lessons_students or []), {})
        teacher_data = self.lessons_teacher
        first_name_student = getattr(student_data, 'first_name', "")
        last_name_student = getattr(student_data, 'last_name', "")
        teacher_user = getattr(teacher_data, 'user', "")
        first_name_teacher = getattr(teacher_user, 'first_name', "")
        last_name_teacher = getattr(teacher_user, 'last_name', "")
        studentName = f'{first_name_student} {last_name_student}'
        teacherName = f'{first_name_teacher} {last_name_teacher}'
        return {
            "id": self.id,
            "title": self.title,
            "color": self.get_colors.get(self.status.value, ""),
            "completionNotes": self.completion_notes,
            "studentName": studentName,
            "teacherName": teacherName,
            "studentId": {"code": getattr(student_data, "id", ""), "label": studentName},
            "teacherId": {"code": getattr(teacher_data, "id", ""), "label": teacherName},
            "description": self.description,
            "status": self.status.value,
            "from_time": self.from_time,
            "to_time": self.to_time,
            "trial_lesson": self.trial_lesson,
            "paid": self.paid,
        }

    def to_dict(self):
        """ Return a dictionary representation of the Lesson object, 
        including teacher and student information."""
        student_data = self.lessons_students[0].to_calendar(
        ) if self.lessons_students else {}
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "last_updated": self.last_updated,
            "completed_at": self.completed_at,
            "space": self.space,
            "from_time": self.from_time,
            "to_time": self.to_time,
            "description": self.description,
            "completion_notes": self.completion_notes,
            "trial_lesson": self.trial_lesson,
            "paid": self.paid,
            "duration_in_minutes": self.duration_in_minutes,
            "status": self.status.value,
            "wage": self.wage,
            "lesson_reminder_sent_at": self.lesson_reminder_sent_at,
            'student': student_data,
            'teacher': (self.lessons_teacher.to_calendar() or {}),
        }

    @staticmethod
    def get_lesson_by_id(id):
        """Retrieve a Lesson object by its id."""
        return Lesson.query.get(id)

    @staticmethod
    def get_all_lessons_for_student(student_id, start_date=None, end_date=None):
        """Retrieve all Lesson objects for a given student id."""
        from models.student import Student
        user = User.query.get(student_id) or abort(404)
        if user.student:
            if start_date is not None and end_date is not None:
                start_date_time = datetime(
                    start_date.year, start_date.month, start_date.day, 1)
                end_date_time = datetime(
                    end_date.year, end_date.month, end_date.day, 1)
                lessons = Lesson.query.options(joinedload(Lesson.lessons_students),
                                               joinedload(Lesson.lessons_teacher)).\
                    join(Lesson.lessons_students).\
                    join(User).\
                    filter(User.uid == Student.user_id).\
                    filter_by(uid=student_id).\
                    filter(Lesson.from_time.between(start_date_time, end_date_time), Lesson.status != LessonStatus.EXPIRED).\
                    order_by(Lesson.from_time.asc()).all()
                return lessons or []
            else:
                student_lessons = Lesson.query.join(Lesson.lessons_students).\
                    join(User).\
                    filter(User.uid == Student.user_id, Lesson.status != LessonStatus.EXPIRED).\
                    filter_by(uid=student_id).\
                    order_by(Lesson.from_time.asc()).all()
                return student_lessons or []
        else:
            abort(404)

    @staticmethod
    def get_all_lessons_for_teacher(teacher_id, start_date, end_date):
        """Retrieve all Lesson objects for a given customer id."""
        user = User.query.get(teacher_id) or abort(404)
        if start_date is not None and end_date is not None:
            start_date_time = datetime(
                start_date.year, start_date.month, start_date.day, 1)
            end_date_time = datetime(
                end_date.year, end_date.month, end_date.day, 1)
            lessons = Lesson.query.\
                options(joinedload(Lesson.lessons_students),
                        joinedload(Lesson.lessons_teacher)).\
                filter_by(teacher_id=user.teacher.id).\
                filter(Lesson.from_time.between(start_date_time, end_date_time),
                       Lesson.status != LessonStatus.EXPIRED).\
                order_by(Lesson.from_time.asc()).all()
            return lessons
        else:
            lessons = Lesson.query.\
                filter_by(teacher_id=user.teacher.id).\
                filter(Lesson.status != LessonStatus.EXPIRED).\
                order_by(Lesson.from_time.asc()).all()
            return lessons

    @staticmethod
    def get_all_lessons_for_a_customer(customer_id, start_date=None, end_date=None):
        """Updates a lesson by the User id from the DB."""
        user = User.query.get(customer_id) or abort(404)
        from models.student import Student
        from models.customer import Customer
        if start_date is not None and end_date is not None:
            start_date_time = datetime(
                start_date.year, start_date.month, start_date.day, 1)
            end_date_time = datetime(
                end_date.year, end_date.month, end_date.day, 1)
            lessons = Lesson.query.\
                options(joinedload(Lesson.lessons_students),
                        joinedload(Lesson.lessons_teacher)).\
                join(Lesson.lessons_students).\
                join(Customer).\
                join(User).\
                filter(User.uid == Customer.user_id).\
                filter_by(uid=customer_id).\
                filter(Lesson.from_time.between(start_date_time, end_date_time),
                       Lesson.status != LessonStatus.EXPIRED).\
                order_by(Lesson.from_time.asc()).all()
            return lessons
        else:
            lessons = Lesson.query.join(Lesson.lessons_students).\
                join(Customer).\
                join(User).\
                filter(User.uid == Customer.user_id,
                       Lesson.status != LessonStatus.EXPIRED).\
                filter_by(uid=customer_id).\
                order_by(Lesson.from_time.asc()).all()
            return lessons

    @staticmethod
    def update_lesson(id=int, **kwargs):
        """Updates a lesson by the User id from the DB"""
        lesson_query = Lesson.query.get(id)
        Lesson.update(lesson_query, kwargs)
        db.session.commit()
        return lesson_query

    @staticmethod
    def add_new_lesson(**kwargs):
        """ Adds a new lesson to the DB. 

        Accepted parameters:
        student_id
        teacher_id
        from_time
        to_time
        space
        description
        title
        """
        from models.teacher import Teacher
        # Get the student
        student = student_module.Student(
        ).get_student_by_id(kwargs['student_id'])
        # Get the teacher
        teacher = Teacher().get_teacher_by_id(kwargs['teacher_id'])
        # Create the lesson
        start_time = kwargs['from_time']
        end_time = kwargs['to_time']

        # Create the Lesson Space URL
        lesson_url = create_lesson_space(teacher, student)

        # Create the Lesson
        lesson = Lesson(space=lesson_url['space'], description=kwargs.get('description'), title=kwargs['title'],
                        teacher_id=kwargs['teacher_id'], from_time=start_time, to_time=end_time)

        # Saving the Lesson Space IDs
        lesson.space_id = lesson_url['room_id']
        lesson.secret = lesson_url['secret']
        lesson.session_id = lesson_url['session_id']

        # Set the duration and wage
        lesson.duration_in_minutes = round(
            (end_time-start_time).total_seconds()/60)
        lesson.wage = (lesson.duration_in_minutes/60)*teacher.wage_per_hour
        lesson.teacher_id = teacher.id
        student.lessons.append(lesson)
        db.session.add(lesson)
        db.session.add(student)
        db.session.commit()
        return lesson

    @staticmethod
    def reschedule_lesson(id, from_time, to_time):
        """Reschedule a lesson by updating its start and end times."""
        lesson = Lesson.get_lesson_by_id(id)
        teacher = lesson.lessons_teacher
        lesson.completed_at = None
        lesson.completion_notes = None
        students = lesson.lessons_students
        lessons = []
        for i in students:
            customer = i.customer
            if lesson in i.lessons:
                newTime = (to_time-from_time).total_seconds()/60
                customer.balance[0].hours_scheduled = customer.balance[0].hours_scheduled - \
                    lesson.duration_in_minutes/60 + newTime/60
                lesson.duration_in_minutes = newTime
        lesson.wage = (lesson.duration_in_minutes/60)*teacher.wage_per_hour
        lesson.status = LessonStatus.SCHEDULED

        db.session.add(lesson)
        db.session.commit()
        return lesson

    @staticmethod
    def delete_lesson(id=str):
        """Deletes a lesson from the DB"""
        lesson = Lesson.query.get(id) or abort(404)
        teacher = lesson.lessons_teacher
        lesson_for_return = lesson.to_dict()
        db.session.delete(lesson)
        db.session.commit()
        return lesson_for_return

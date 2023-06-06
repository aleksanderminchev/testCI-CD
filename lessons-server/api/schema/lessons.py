
from datetime import datetime, timezone

from flask import request
from marshmallow import validate, validates, validates_schema, \
    ValidationError, fields

from api import ma
from pytz import utc
from api.auth import token_auth
from models.lesson import Lesson
from models.teacher import Teacher, Student
from api.schema.teacher.teachers import TeacherSchema
from api.schema.student import StudentSchema
from api.utils.utils import get_date
from models.user import User


class LessonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True
    id = ma.Integer(dump_only=True)
    title = ma.String(dump_only=True)
    space = ma.String(dump_only=True)
    duration_in_minutes = ma.Integer(dump_only=True)
    description = ma.String(dump_only=True)
    completion_notes = ma.String(dump_only=True)
    wage = ma.Float(dump_only=True)
    status = ma.String(dump_only=True)
    paid = ma.Boolean(dump_only=True)
    trial_lesson = ma.Boolean(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    completed_at = ma.DateTime(dump_only=True)
    from_time = ma.DateTime(dump_only=True)
    to_time = ma.DateTime(dump_only=True)
    lesson_reminder_sent_at = ma.DateTime(dump_only=True)
    teacher = fields.Nested(TeacherSchema(), dump_only=True)
    student = fields.Nested(StudentSchema(), dump_only=True)


class CancelLessonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True
    lesson_id = ma.Integer(required=True)
    cancellation_reason = ma.String(required=True, validate=validate.OneOf(
        ['bad cancellation student', 'bad cancellation teacher', 'good cancellation']))
    id = ma.Integer(dump_only=True)
    title = ma.String(dump_only=True)
    space = ma.String(dump_only=True)
    duration_in_minutes = ma.Integer(dump_only=True)
    wage = ma.Float(dump_only=True)
    status = ma.String(dump_only=True)
    description = ma.String(dump_only=True)
    completion_notes = ma.String(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    completed_at = ma.DateTime(dump_only=True)
    trial_lesson = ma.Boolean(dump_only=True)
    from_time = ma.DateTime(dump_only=True)
    to_time = ma.DateTime(dump_only=True)
    lesson_reminder_sent_at = ma.DateTime(dump_only=True)
    teacher = fields.Nested(TeacherSchema(), dump_only=True)
    student = fields.Nested(StudentSchema(), dump_only=True)

    @validates('lesson_id')
    def validate_lesson_id(self, value):
        lesson = Lesson.get_lesson_by_id(value)
        age = lesson.to_time
        todayDate = datetime.now()

        # previousMonthDate=todayDate.replace(day=16,month=todayDate.month-1)
        thisMonthDate = todayDate.replace(
            day=15, hour=23, minute=59, second=59)
        user = User.verify_access_token(
            request.headers['Authorization'].split(' ')[1]).is_admin or False
        if lesson is None:
            raise ValidationError('No lesson was found')
        elif lesson.paid:
            raise ValidationError(
                'Lesson cannot be edited because it has been paid for')
        elif age <= thisMonthDate and todayDate > thisMonthDate:
            raise ValidationError(
                'Trying to create within previous wage period')
        elif (datetime.now() - age).total_seconds()/60/60/24 >= 7 and not user:
            raise ValidationError(
                'Cannot create a lesson more than 7 days ago')


class CreateLessonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True

    # Required
    teacher_id = ma.Integer(required=True)
    student_id = ma.Integer(required=True)
    title = ma.String(required=True)
    from_time = ma.DateTime(required=True, description='Format in utc time', validate=[
                            lambda x:x.tzinfo == timezone.utc])
    to_time = ma.DateTime(required=True, description='Format in utc time', validate=[
                          lambda x:x.tzinfo == timezone.utc])

    # Optional
    trial_lesson = ma.Boolean(required=False)
    description = ma.String(required=False)

    # Dump only
    status = ma.String(dump_only=True, description='Status of the lesson should start as scheduled',
                       validate=validate.OneOf(['scheduled']))
    duration_in_minutes = ma.Integer(dump_only=True)
    wage = ma.Float(dump_only=True)
    completed_at = ma.DateTime(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    id = ma.String(dump_only=True)
    completion_notes = ma.String(dump_only=True)
    space = ma.String(dump_only=True)
    lesson_reminder_sent_at = ma.DateTime(dump_only=True)
    teacher = fields.Nested(TeacherSchema(), dump_only=True)
    student = fields.Nested(StudentSchema(), dump_only=True)

    @validates_schema
    def validate_not_in_previous_payment_cycle(self, data, **kwargs):
        """ Validates that the Lesson dates are not in previous wage period.
        Teachers can only create lessons that are less than 7 days old.
        Admins can create older lessons, but only as long as they're not in the previous wage period.
        """
        from_time = data.get('from_time')
        user = User.verify_access_token(
            request.headers['Authorization'].split(' ')[1]).is_admin or False
        todayDate = datetime.now(timezone.utc)
        thisMonthDate = todayDate.replace(
            day=15, hour=23, minute=59, second=59)
        if from_time <= thisMonthDate and todayDate > thisMonthDate:
            raise ValidationError(
                'Trying to create within previous wage period')
        elif (datetime.now() - from_time.replace(tzinfo=None)).total_seconds()/60/60/24 >= 7 and not user:
            raise ValidationError(
                'Cannot create a lesson more than 7 days ago')

    @validates_schema
    def validate_student_is_taught_by_teacher(self, data, **kwargs):
        """ Validates that the student is assigned to the teacher. """
        teacher = Teacher.get_teacher_by_id(data.get('teacher_id')) or None
        student = Student.get_student_by_id(data.get('student_id')) or None
        if student not in teacher.students:
            raise ValidationError('Student is not assigned to the teacher')

    @validates_schema
    def validate_time_input(self, data, **kwargs):
        """ Validates lesson length. Has to be more than 0 minutes and less than 10 hours. """
        from_time = data.get('from_time')
        to_time = data.get('to_time')
        total_time = (to_time-from_time).total_seconds()/60
        if total_time <= 0:
            raise ValidationError('Times given are not valid')
        elif total_time/60 > 10:
            raise ValidationError('Time is more than 10 hours')

    @validates_schema
    def validate_time_of_teacher_is_not_taken_from_time(self, data, **kwargs):
        """ Validates the from_time to check that the teacher is not already scheduled with a student, so there are no overlaps. """
        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson_from_time = Lesson.query.filter_by(
            teacher_id=data.get('teacher_id'), from_time=from_time).first()
        lesson_to_time = Lesson.query.filter_by(
            teacher_id=data.get('teacher_id'), to_time=from_time).first()
        lesson_between_from_time = Lesson.query.filter_by(teacher_id=data.get(
            'teacher_id')).filter(Lesson.from_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter_by(teacher_id=data.get('teacher_id')).filter(
            Lesson.from_time <= from_time, Lesson.to_time >= from_time).all()

        if lesson_from_time is not None:
            raise ValidationError('Time for lesson is not available')
        elif lesson_to_time is not None:
            raise ValidationError('Time for lesson is not available')
        elif len(lesson_between_from_time) != 0 or len(lesson_db_between) != 0:
            raise ValidationError(
                'Time between lesson for teacher is not available')

    @validates_schema
    def validate_time_of_teacher_is_not_taken_to_time(self, data, **kwargs):
        """ Validates the to_time to check that the teacher is not already scheduled with a student, so there are no overlaps. """

        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson_from_time = Lesson.query.filter_by(
            teacher_id=data.get('teacher_id'), from_time=to_time).first()
        lesson_to_time = Lesson.query.filter_by(
            teacher_id=data.get('teacher_id'), to_time=to_time).first()
        lesson_between_to_time = Lesson.query.filter_by(teacher_id=data.get(
            'teacher_id')).filter(Lesson.to_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter_by(teacher_id=data.get('teacher_id')).filter(
            Lesson.from_time <= to_time, Lesson.to_time >= to_time).all()

        if lesson_from_time is not None:
            raise ValidationError('Time for lesson is not available')
        elif lesson_to_time is not None:
            raise ValidationError('Time for lesson is not available')
        elif len(lesson_between_to_time) != 0 or len(lesson_db_between) != 0:
            raise ValidationError(
                'Time between lesson for teacher is not available')

    @validates_schema
    def validate_time_of_student_is_not_taken_to_time(self, data, **kwargs):
        """ Validates the to_time to check that the student is not already scheduled with a tutor, so there are no overlaps. """

        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson_from_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=data.get('student_id')), Lesson.from_time == to_time).first()
        lesson_to_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=data.get('student_id')), Lesson.to_time == to_time).first()
        lesson_between_to_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=data.get('student_id')), Lesson.to_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter(Lesson.lessons_students.any(id=data.get(
            'student_id')), Lesson.from_time <= to_time, Lesson.to_time >= to_time).all()

        if lesson_from_time is not None:
            raise ValidationError('Time for lesson is not available student')
        elif lesson_to_time is not None:
            raise ValidationError('Time for lesson is not available student')
        elif len(lesson_between_to_time) != 0 or len(lesson_db_between) != 0:
            raise ValidationError(
                'Time between lesson for student is not available')

    @validates_schema
    def validate_time_of_student_is_not_taken_from_time(self, data, **kwargs):
        """ Validates the from_time to check that the student is not already scheduled with a tutor, so there are no overlaps. """
        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson_from_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=data.get('student_id')), Lesson.from_time == from_time).first()
        lesson_to_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=data.get('student_id')), Lesson.to_time == from_time).first()
        lesson_between_from_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=data.get('student_id')), Lesson.from_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter(Lesson.lessons_students.any(id=data.get(
            'student_id')), Lesson.from_time <= from_time, Lesson.to_time >= from_time).all()

        if lesson_from_time is not None:
            raise ValidationError('Time for lesson is not available student')
        elif lesson_to_time is not None:
            raise ValidationError('Time for lesson is not available student')
        elif len(lesson_between_from_time) != 0 or len(lesson_db_between) != 0:
            raise ValidationError(
                'Time between lesson for student is not available')

    @validates('teacher_id')
    def validate_teacher_id(self, value):
        """ Validates tha the teacher id exists. """
        if Teacher.get_teacher_by_id(value) is None:
            raise ValidationError('No teacher was found')

    @validates('student_id')
    def validate_student_id(self, value):
        """ Validates tha the student id exists. """
        if Student.get_student_by_id(value) is None:
            raise ValidationError('No student was found')


class UpdateLessonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True
    id = ma.Integer(required=True)
    from_time = ma.DateTime(description='Format in utc time,time shouldnt exist already for this teacher and student', validate=[
                            lambda x:x.tzinfo == timezone.utc])
    to_time = ma.DateTime(description='Format in utc time,time shouldnt exist already for this teacher and student', validate=[
                          lambda x:x.tzinfo == timezone.utc])
    lesson_reminder_sent_at = ma.DateTime(description='Format in utc time', validate=[
                                          lambda x:x.tzinfo == timezone.utc])
    completed_at = ma.DateTime()
    space = ma.String()
    title = ma.String()
    paid = ma.Boolean(dump_only=True)
    trial_lesson = ma.Boolean(required=False)
    duration_in_minutes = ma.Integer()
    description = ma.String(required=False)
    completion_notes = ma.String(required=False)
    status = ma.String(description='Status of the lesson should start as scheduled', validate=validate.OneOf(
        ['scheduled', 'attended', 'bad cancellation student', 'bad cancellation teacher', 'good cancellation']))
    wage = ma.Float(dump_only=True)
    created_at = ma.DateTime(dump_only=True)
    last_updated = ma.DateTime(dump_only=True)
    teacher = fields.Nested(TeacherSchema(), dump_only=True)
    student = fields.Nested(StudentSchema(), dump_only=True)

    @validates('id')
    def validate_lesson_id(self, value):
        lesson = Lesson.get_lesson_by_id(value)
        age = lesson.to_time
        todayDate = datetime.now()
        # previousMonthDate=todayDate.replace(day=16,month=todayDate.month-1)
        user = User.verify_access_token(
            request.headers['Authorization'].split(' ')[1]).is_admin or False

        thisMonthDate = todayDate.replace(
            day=15, hour=23, minute=59, second=59)
        if lesson is None:
            raise ValidationError('No lesson was found')
        elif lesson.paid:
            raise ValidationError(
                'Lesson cannot be edited because it has been paid for')
        elif age <= thisMonthDate and todayDate > thisMonthDate:
            raise ValidationError(
                'Trying to create within previous wage period')
        elif (datetime.now() - age).total_seconds()/60/60/24 >= 7 and not user:
            raise ValidationError(
                'Cannot create a lesson more than 7 days ago')

    @validates_schema
    def validate_time_input(self, data, **kwargs):
        from_time = data.get('from_time')
        to_time = data.get('to_time')
        total_time = (to_time-from_time).total_seconds()/60
        if total_time <= 0:
            raise ValidationError('Times given are not valid')
        elif total_time/60 > 10:
            raise ValidationError('Time is more than 10 hours')

    @validates_schema
    def validate_time_of_teacher_is_not_taken_from_time(self, data, **kwargs):
        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson = Lesson.query.get(data.get('id'))
        lesson_from_time = Lesson.query.filter_by(
            teacher_id=lesson.teacher_id, from_time=from_time).first()
        lesson_to_time = Lesson.query.filter_by(
            teacher_id=lesson.teacher_id, to_time=from_time).first()
        lesson_between_from_time = Lesson.query.filter_by(teacher_id=lesson.teacher_id).filter(
            Lesson.from_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter_by(teacher_id=lesson.teacher_id).filter(
            Lesson.from_time <= from_time, Lesson.to_time >= from_time).all()
        if lesson in lesson_between_from_time:
            lesson_between_from_time.remove(lesson)
        if lesson in lesson_db_between:
            lesson_db_between.remove(lesson)
        if lesson_from_time is not None:
            if lesson_from_time is not lesson:
                raise ValidationError('Time for lesson is not available')
        elif lesson_to_time is not None:
            if lesson_to_time is not lesson:
                raise ValidationError('Time for lesson is not available')
        elif all(lesson is not x for x in lesson_between_from_time) and len(lesson_between_from_time) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')
        elif all(lesson is not x for x in lesson_db_between) and len(lesson_db_between) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')

    @validates_schema
    def validate_time_of_teacher_is_not_taken_to_time(self, data, **kwargs):
        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson = Lesson.query.get(data.get('id'))
        lesson_from_time = Lesson.query.filter_by(
            teacher_id=lesson.teacher_id, from_time=to_time).first()
        lesson_to_time = Lesson.query.filter_by(
            teacher_id=lesson.teacher_id, to_time=to_time).first()
        lesson_between_to_time = Lesson.query.filter_by(teacher_id=lesson.teacher_id).filter(
            Lesson.to_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter_by(teacher_id=lesson.teacher_id).filter(
            Lesson.from_time <= to_time, Lesson.to_time >= to_time).all()

        if lesson in lesson_between_to_time:
            lesson_between_to_time.remove(lesson)
        if lesson in lesson_db_between:
            lesson_db_between.remove(lesson)

        if lesson_from_time is not None:
            if lesson_from_time is not lesson:
                raise ValidationError('Time for lesson is not available')
        elif lesson_to_time is not None:
            if lesson_to_time is not lesson:
                raise ValidationError('Time for lesson is not available')
        elif all(lesson is not x for x in lesson_between_to_time) and len(lesson_between_to_time) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')
        elif all(lesson is not x for x in lesson_db_between) and len(lesson_db_between) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')

    @validates_schema
    def validate_time_of_student_is_not_taken_to_time(self, data, **kwargs):
        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson = Lesson.query.get(data.get('id'))
        lesson_from_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.from_time == to_time).first()
        lesson_to_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.to_time == to_time).first()
        lesson_between_to_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.to_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.from_time <= to_time, Lesson.to_time >= to_time).all()
        if lesson in lesson_between_to_time:
            lesson_between_to_time.remove(lesson)
        if lesson in lesson_db_between:
            lesson_db_between.remove(lesson)
        if lesson_from_time is not None:
            if lesson_from_time is not lesson:
                raise ValidationError(
                    'Time for lesson is not available student')
        elif lesson_to_time is not None:
            if lesson_to_time is not lesson:
                raise ValidationError(
                    'Time for lesson is not available student')
        elif all(lesson is not x for x in lesson_between_to_time) and len(lesson_between_to_time) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')
        elif all(lesson is not x for x in lesson_db_between) and len(lesson_db_between) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')

    @validates_schema
    def validate_time_of_student_is_not_taken_from_time(self, data, **kwargs):
        to_time = data.get('to_time').replace(tzinfo=None)
        from_time = data.get('from_time').replace(tzinfo=None)
        lesson = Lesson.query.get(data.get('id'))
        lesson_from_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.from_time == from_time).first()
        lesson_to_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.to_time == from_time).first()
        lesson_between_from_time = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.from_time.between(from_time, to_time)).all()
        lesson_db_between = Lesson.query.filter(Lesson.lessons_students.any(
            id=lesson.lessons_students[0].id), Lesson.from_time <= from_time, Lesson.to_time >= from_time).all()
        if lesson in lesson_between_from_time:
            lesson_between_from_time.remove(lesson)
        if lesson in lesson_db_between:
            lesson_db_between.remove(lesson)
        if lesson_from_time is not None:
            if lesson_from_time is not lesson:
                raise ValidationError(
                    'Time for lesson is not available student')
        elif lesson_to_time is not None:
            if lesson_to_time is not lesson:
                raise ValidationError(
                    'Time for lesson is not available student')
        elif all(lesson is not x for x in lesson_between_from_time) and len(lesson_between_from_time) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')
        elif all(lesson is not x for x in lesson_db_between) and len(lesson_db_between) >= 1:
            raise ValidationError(
                'Time between lesson for teacher is not available')


class CompleteLessonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True
    id = ma.Integer(required=True)
    status = ma.String(required=True, description='Status of the lesson should start as scheduled',
                       validate=validate.OneOf(['attended']))
    completion_notes = ma.String(
        required=True, description='Some notes that can be entered')

    @validates('id')
    def validate_student_id(self, value):
        lesson = Lesson.get_lesson_by_id(value)
        if lesson is None:
            raise ValidationError('No lesson was found')
        elif lesson.status.value != 'scheduled':
            raise ValidationError('Lesson cannot be completed')

        age = lesson.to_time
        todayDate = datetime.now()
        # previousMonthDate=todayDate.replace(day=16,month=todayDate.month-1)
        user = User.verify_access_token(
            request.headers['Authorization'].split(' ')[1]).is_admin or False
        thisMonthDate = todayDate.replace(
            day=15, hour=23, minute=59, second=59)
        if lesson is None:
            raise ValidationError('No lesson was found')
        elif lesson.paid:
            raise ValidationError(
                'Lesson cannot be edited because it has been paid for')
        elif age <= thisMonthDate and todayDate > thisMonthDate:
            raise ValidationError(
                'Trying to update within previous wage period')
        elif (datetime.now() - age).total_seconds()/60/60/24 >= 7 and not user:
            raise ValidationError(
                'Cannot update a lesson more than 7 days ago')


class RescheduledLesson(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True
    id = ma.Integer(required=True)
    from_time = ma.DateTime(description='Format in utc time,time shouldnt exist already for this teacher and student', validate=[
                            lambda x:x.tzinfo == timezone.utc])
    to_time = ma.DateTime(description='Format in utc time,time shouldnt exist already for this teacher and student', validate=[
                          lambda x:x.tzinfo == timezone.utc])

    @validates_schema
    def validate_time_input(self, data, **kwargs):
        from_time = data.get('from_time')
        to_time = data.get('to_time')
        total_time = (to_time-from_time).total_seconds()/60
        if total_time <= 0:
            raise ValidationError('Times given are not valid')
        elif total_time/60 > 10:
            raise ValidationError('Time is more than 10 hours')

    @validates('id')
    def validate_teacher_id(self, value):
        if Lesson.get_lesson_by_id(value) is None:
            raise ValidationError('No lesson was found')


class PlaybackUrlSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Lesson
        ordered = True
    name = ma.String(dump_only=True)
    url = ma.String(dump_only=True)
    teacher_name = ma.String(dump_only=True)
    student_name = ma.String(dump_only=True)
    start_time = ma.String(dump_only=True)
    end_time = ma.String(dump_only=True)


class StudentTeacherIdCalendar(ma.Schema):
    class Meta:
        ordered = True

    code = ma.String(dump_only=True)
    label = ma.String(dump_only=True)


class CalendarLessons(ma.Schema):
    class Meta:
        model = Lesson
        ordered = True

    from_date = ma.Date(required=False, load_only=True)
    to_date = ma.Date(required=False, load_only=True)
    to_time = ma.DateTime(dump_only=True)
    from_time = ma.DateTime(dump_only=True)
    id = ma.Integer(dump_only=True)
    title = ma.String(dump_only=True)
    color = ma.String(dump_only=True)
    status = ma.String(dump_only=True)
    completionNotes = ma.String(dump_only=True)
    description = ma.String(dump_only=True)
    studentName = ma.String(dump_only=True)
    teacherName = ma.String(dump_only=True)
    studentId = fields.Nested(StudentTeacherIdCalendar(), dump_only=True)
    teacherId = fields.Nested(StudentTeacherIdCalendar(), dump_only=True)
    trial_lesson = ma.Boolean(dump_only=True)
    paid = ma.Boolean(dump_only=True)

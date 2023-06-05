import enum
from api.app import db
from api.utils.utils import Updateable, get_date
from models.user import User
from models.lesson import student_lessons
from flask import abort, render_template, current_app
from api.email import send_email


class StudentTypeEnum(enum.Enum):
    """ To add this type in migration add:
    from sqlalchemy.dialects import postgresql
    student_type = postgresql.ENUM('child', 'independent', name='studenttypeenum')
    student_type.create(op.get_bind())
    """
    CHILD = 'child'
    INDEPENDENT = 'independent'


class GenderEnum(enum.Enum):
    """ To add this type in migration add:
        Female enum may have an issue in the database. When I tested it didn't allow to add entries with 'female' as gender.
        Female was in the db's enum. Manually added it for it to work properly. For some reason it adds a space to 'female '.
        from sqlalchemy.dialects import postgresql
        gender_enum = postgresql.ENUM('male', 'female', name='genderenum')
        gender_enum.create(op.get_bind())
    """
    MALE = "male"
    FEMALE = "female"


class StatusEnum(enum.Enum):
    """ To add this type in migration add:
        from sqlalchemy.dialects import postgresql
        student_status = postgresql.ENUM('active', 'inactive', name='statusstudent')
        student_status.create(op.get_bind())
    """
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Student(Updateable, db.Model):  # type:ignore
    """
    Model for Students.
    Relation to one user.
    Relation to one, or more parents (Many-to-Many)
    Related to none, one, or more Teachers (Many-to-Many)
    Related to none, one, or more lessons (Many-to-Many)
    """

    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    # Many-to-Many relationship to Teachers through lessons
    lessons = db.relationship("Lesson", secondary=student_lessons, primaryjoin=(
        student_lessons.c.student_id == id), backref='lessons_students')
    # One-to-one relation to a User Account
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), index=True)
    # Many to Many students-teachers relation

    # One Customer to Many students relation
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False, index=True)
    customer = db.relationship("Customer", backref="students")
    # Active/Inactive
    status = db.Column(
        db.Enum(
            StatusEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=StatusEnum.INACTIVE.value,
        server_default=StatusEnum.INACTIVE.value,
        index=True
    )
    # Male/Female
    gender = db.Column(
        db.Enum(
            GenderEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=GenderEnum.MALE.value,
        server_default=GenderEnum.MALE.value,
        index=True
    )
    first_name = db.Column(db.String(256), nullable=True)
    last_name = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(256), nullable=True, index=True)
    email_lesson_reminder = db.Column(
        db.Boolean(), default=True, server_default='t', nullable=False)
    email_lesson_notes = db.Column(
        db.Boolean(), default=True, server_default='t', nullable=False)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    student_type = db.Column(
        db.Enum(
            StudentTypeEnum,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=StudentTypeEnum.INDEPENDENT.value,
        server_default=StudentTypeEnum.INDEPENDENT.value,
        index=True
    )
    # teachers = db.relationship("Teacher", secondary=student_teachers, backref="Student") TODO
    # lessons = db.relationship("Lesson", secondary=student_lesson, backref="student") TODO

    def to_dict(self):
        if self.user:
            phone = self.user.phone
        else:
            phone = self.customer.user.phone
        
        return {
            "status": self.status.value,
            "gender": self.gender.value,
            "student_type": self.student_type.value,
            "first_name": self.first_name,
            "email_lesson_reminders": self.email_lesson_reminder,
            "email_lesson_notes": self.email_lesson_notes,
            "last_name": self.last_name,
            "email": self.email,
            'phone': phone,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'teachers': [i.id for i in (self.teachers or [])],
            'customer_id': self.customer_id,
            'id': self.id
        }
        
    def to_calendar(self):
        if self.user:
            phone = self.user.phone
        else:
            phone = self.customer.user.phone
        
        return {
            "status": self.status.value,
            "student_type": self.student_type.value,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            'phone': (self.user or self.customer.user).phone,
            'teachers': [i.id for i in self.teachers] if self.teachers else [],
            'customer_id': self.customer_id,
            'id': self.id
        }
    @staticmethod
    def add_new_student(id=str, typeOfStudent=None, **kwargs):
        """ Adds a new student to the DB. """
        from models.customer import Customer
        if typeOfStudent == 'no_user':
            customer = Customer.query.get(id)
            student = Student(customer_id=id, student_type='child', **kwargs)
            db.session.add(student)
            db.session.commit()
            return student
        elif typeOfStudent == 'with_user':
            # new user here for the student and associated it with the account
            user = User(email=kwargs['email'], password='', first_name=kwargs['first_name'],
                        last_name=kwargs['last_name'], phone=kwargs['phone'])
            db.session.add(user)
            db.session.commit()
            if user is not None:
                reset_token = user.generate_reset_token()
                reset_url = current_app.config['CONFIRMATION_URL'] + \
                    '?token=' + reset_token
                template = render_template(
                    "email/verify-email.html",
                    token=reset_token,
                    confirm_url=reset_url
                )
                send_email([kwargs['email']], 'Confirm your account', template)
            customer = Customer.query.get(id)
            student = Student(user_id=user.uid, customer_id=id, student_type='independent',
                              email=kwargs['email'], first_name=kwargs['first_name'], last_name=kwargs['last_name'])
            db.session.add(student)
            db.session.commit()
            return student
        else:
            raise ValueError('invalid student type')
    @staticmethod
    def delete_student(id=str):
        """Deletes a student from the DB"""
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return student

    @staticmethod
    def get_student_by_id(student_id=int):
        """Gets a student by the id from the DB"""
        return Student.query.get(student_id)

    @staticmethod
    def get_student_by_email(email=str):
        """Gets a student by the email from the DB"""
        user = User.query.filter_by(email=email).first() or abort(404)
        students = set()
        if user.customer:
            for i in user.customer.students:
                students.add(i)
        if user.student:
            students.add(user.student)
        return students

    @staticmethod
    def update_student(id=int, **kwargs):
        """Update student
         Updates a Student and their associated User Account (if they have one). 
         Gets the student by their Student ID
        """

        # Update both the customer and user.
        student = Student.get_student_by_id(id) or abort(404)
        if student.user and student.student_type.value == 'independent':
            arguments_for_user = {}
            for key, value in kwargs.items():
                if key in ('first_name', 'last_name', 'phone', 'email'):
                    arguments_for_user[key] = value
            User.update(student.user, arguments_for_user)
        db.session.commit()
        updated_student = Student.update(student, kwargs)
        db.session.commit()
        return updated_student

    @staticmethod
    def add_teacher_to_student(teacher_id, student_email):
        from models.teacher import Teacher
        student = Student.query.filter_by(email=student_email).first()
        print(teacher_id)
        print(student_email)
        teachers = []
        for i in teacher_id:
            teacher = Teacher.get_teacher_by_id(i)
            teachers.append(teacher)
            print(teachers)
            student.teachers = teachers
            db.session.add(student)
            db.session.commit()
        return student.teachers

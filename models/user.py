import jwt

from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from time import time
from sqlalchemy.orm import validates
from api.utils.utils import get_date, Updateable
from api.app import db
from models.token import Token


class User(Updateable, db.Model):  # type:ignore
    """ The DB model for users.

    Has all the common user fields.

    Relationship to Tokens (One user to many tokens)
    """

    __tablename__ = "users"

    # general
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)

    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    is_verified = db.Column(db.Boolean, default=False, index=True)
    verified_time = db.Column(db.DateTime)
    teacher = db.relationship("Teacher", backref="user", uselist=False)
    customer = db.relationship("Customer", backref="user", uselist=False)
    student = db.relationship("Student", backref="user", uselist=False)
    tokens = db.relationship(
        'Token',
        back_populates='user',
        lazy='noload'
    )

    first_name = db.Column(db.String(256), nullable=True)
    last_name = db.Column(db.String(256), nullable=True)
    phone = db.Column(db.String(256))
    last_login = db.Column(db.DateTime, default=get_date)

    def __repr__(self):  # pragma: no cover
        return '<User {}>'.format(self.email)

    def exists(self, email):  # check if User email exists in db
        exists = db.session.query(User.uid).filter_by(
            email=email).first() is not None
        return exists

    def ping(self):
        self.last_login = datetime.utcnow()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):  # Hashes the password
        self.password_hash = generate_password_hash(password)

    @validates("first_name")
    def validate_first_name(self, key, first_name):
        if not isinstance(first_name, str):
            raise ValueError("invalid first name")
        if 1 > len(first_name) > 50:
            raise ValueError("invalid first name")
        return first_name

    @validates("last_name")
    def validate_last_name(self, key, last_name):
        if not isinstance(last_name, str):
            raise ValueError("invalid last name")
        if 1 > len(last_name) > 50:
            raise ValueError("invalid last name")

        return last_name

    @validates("email")
    def validate_email(self, key, email):
        if not isinstance(email, str):
            raise ValueError("invalid email")
        if 12 >= len(email) >= 120:
            raise ValueError("invalid email")

        return email

    @validates("phone")
    def validate_phone(self, key, phone):
        if not isinstance(phone, str):
            raise ValueError("invalid phone")
        if 15 <= len(phone) <= 10:
            if phone[0] != '+':
                raise ValueError("invalid phone")
            raise ValueError("invalid phone")
        return phone

    def verify_password(self, password):  # Verifies the hashed password
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        token = Token(user=self)
        token.generate()
        return token

    def generate_jwt_auth_token(self):
        return jwt.encode(
            {"id": self.uid}, current_app.config["SECRET_KEY"], algorithm="HS256"
        )

    @staticmethod
    def verify_access_token(access_token, refresh_token=None):
        token = Token.from_jwt(access_token)
        if token:
            if token.access_expiration > datetime.utcnow():
                print(token.access_expiration)
                if token.user.is_verified:
                    token.user.ping()
                    db.session.commit()
                    return token.user

    @staticmethod
    def verify_refresh_token(refresh_token, access_token_jwt):
        token = Token.from_jwt(access_token_jwt)
        print(token.refresh_token)
        if token and token.refresh_token == refresh_token:
            if token.refresh_expiration > datetime.utcnow():
                print(token.refresh_expiration)
                return token

            # someone tried to refresh with an expired token
            # revoke all tokens from this user as a precaution
            token.user.revoke_all()
            db.session.commit()

    @staticmethod
    def verify_api_jwt_token(token):
        try:
            data = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
        except Exception:
            return None  # error
        return User.query.get(data["id"])

    def routes_allowed(self):
        """Get the routes the user is allowed to access,
        add new routes here that the user is allowed to access
        """
        if self.is_admin:
            return {
                "*"
            }
        elif self.is_customer:
            list_students = set()
            for i in self.customer.students:
                list_students.add(f"/api/students/{i.id}")
                [(list_students.add(f"/api/lesson/{j.id}"), list_students.add(f"/api/lesson_replay/{j.id}"),
                  list_students.add(f"/api/get_lesson_space_url_student/{j.id}")) for j in i.lessons or []]
                [(list_students.add(f"/api/teachers/{j.id}"), list_students.add(
                    "/api/teachers/"+j.user.email))for j in i.teachers or []]
            [list_students.add(f"/api/order/{j.uid}")
             for j in self.customer.orders or []]
            [list_students.add(f"/api/transaction/{j.id}")
             for j in self.customer.transactions or []]
            basic_routes_list = {
                "/api/users/"+self.get_id(),
                "/api/users/"+self.email,
                "/api/tokens",
                "/api/me",
                "/api/get_all_programmes",
                "/api/get_all_institutions",
                "/api/get_all_highschools",
                f"/api/transactions_customer/{self.customer.id}",
                "/api/subjectss",
                "/api/programs",
                "/api/order",
                "/api/languages",
                "/api/interests",
                "/api/transaction",
                "/api/qualifications",
                f"/api/get_balance/{self.customer.id}",
                f"/api/orders_customer/{self.customer.id}",
                "/api/customer",
                f"/api/customers/{self.customer.id}",
                "/api/customers/"+self.email,
                "/api/student",
                "/api/students",
                "/api/students/"+self.email,
                "/api/get_all_teachers/"+self.email,
            }
            union_list = list_students.union(basic_routes_list)
            return union_list

        elif self.is_teacher:
            list_students = set()

            for i in self.teacher.students:
                list_students.add(f"/api/students/{i.id}")
                if i.user is not None:
                    list_students.add("/api/students/"+i.user.email)
                list_students.add(f"/api/customer/{i.customer.id}")
                list_students.add("/api/student/"+i.customer.user.email)
            [(list_students.add(f"/api/lesson/{j.id}"), list_students.add(f"/api/lesson_replay/{j.id}"),
              list_students.add(f"/api/get_lesson_space_url_teacher/{j.id}")) for j in self.teacher.lessons_teacher or []]

            [(list_students.add(f"/api/wagepayments/{j.id}"))
             for j in self.teacher.wagepayments or []]
            basic_routes_list = {
                "/api/users/"+self.get_id(),
                "/api/users/"+self.email,
                "/api/tokens",
                "/api/me",
                f"/api/tutor_wagepayments/{self.teacher.id}",
                "/api/wagepayments",
                "/api/get_all_programmes",
                "/api/get_all_institutions",
                "/api/get_all_highschools",
                "/api/subjectss",
                "/api/programs",
                "/api/order",
                "/api/languages",
                "/api/interests",
                "/api/qualifications",
                "/api/teacher",
                f"/api/teachers/{self.teacher.id}",
                "/api/teachers/"+self.email,
                "/api/get_all_students/"+self.email,
                "/api/complete_lessons",
                "/api/cancel_lesson",
                "/api/reschedule_lesson"
            }
            union_list = list_students.union(basic_routes_list)
            return union_list
        elif self.is_student:
            list_students = set()
            [(list_students.add(f"/api/lesson/{j.id}"), list_students.add(f"/api/lesson_replay/{j.id}"),
             list_students.add(f"/api/get_lesson_space_url_student/{j.id}")) for j in self.student.lessons or []]
            for i in self.student.teachers:
                list_students.add(f"/api/teachers/{i.id}")
            [list_students.add(f"/api/order/{j.uid}")
             for j in self.student.customer.orders or []]
            basic_routes_list = {
                "/api/users/"+self.get_id(),
                "/api/users/"+self.email,
                "/api/tokens",
                "/api/me",
                f"/api/students/{self.student.id}",
                "/api/get_all_programmes",
                "/api/get_all_institutions",
                "/api/get_all_highschools",
                f"/api/transactions_customer/{self.student.customer.id}",
                "/api/subjectss",
                "/api/programs",
                "/api/order",
                "/api/languages",
                "/api/interests",
                "/api/qualifications",
                f"/api/get_balance/{self.student.customer.id}",
                f"/api/orders_customer/{self.student.customer.id}",
                f"/api/customers/{self.student.customer.id}",
                f"/api/customers/{self.student.customer.user.email}",
                "/api/student",
                "/api/students/"+self.email,
                "/api/get_all_teachers/"+self.email,
            }
            union_list = list_students.union(basic_routes_list)
            return union_list

    def revoke_all(self):
        Token.query.filter(Token.user == self).delete()

    def generate_reset_token(self):
        return jwt.encode(
            {
                'exp': time() + current_app.config['RESET_TOKEN_MINUTES'] * 60,
                'reset_email': self.email,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_token(reset_token):
        try:
            data = jwt.decode(reset_token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except jwt.PyJWTError:
            return
        return User.query.filter_by(email=data['reset_email']).first()

    def to_dict(self):
        # Exports Users data from db to a dictionary
        student_dict = None
        if self.student is not None:
            student_dict = self.student.to_dict()

        teacher_dict = None
        if self.teacher is not None:
            teacher_dict = self.teacher.to_dict()

        customer_dict = None
        if self.customer is not None:
            customer_dict = self.customer.to_dict()

        return {
            "uid": self.uid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            'phone': self.phone,
            'is_verified': self.is_verified,
            'last_login': self.last_login,
            "email": self.email,
            "last_updated": self.last_updated,
            "created_at": self.created_at,
            "admin": self.is_admin,
            "student": self.is_student,
            "student_dict": student_dict,
            "teacher": self.is_teacher,
            "teacher_dict": teacher_dict,
            "customer": self.is_customer,
            "customer_dict": customer_dict,
            'roles': self.get_roles
        }

    @staticmethod
    def get_user(email, password):
        user = User.query.filter_by(email=email).first()
        if user is None or not user.verify_password(password):
            return None
        else:
            return user

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_admin(self):
        if self.admin:
            return True
        return False

    @property
    def is_student(self):
        if self.student:
            return True
        return False

    @property
    def get_roles(self):
        roles = []
        if self.is_customer:
            roles.append('customer')
        elif self.is_student:
            roles.append('student')
        elif self.is_admin:
            roles.append('admin')
        elif self.is_teacher:
            roles.append('teacher')
        return roles

    @property
    def is_teacher(self):
        if self.teacher:
            return True
        return False

    @property
    def is_customer(self):
        if self.customer:
            return True
        return False

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.uid)

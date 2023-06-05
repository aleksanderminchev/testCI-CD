import enum
from flask import abort, render_template, current_app

from api.app import db
from models.user import User
from models.student import Student, StatusEnum
from api.utils.utils import Updateable, get_date
from api.email import send_email
from sqlalchemy.orm import validates


class CustomerType(enum.Enum):
    """ To add this type in migration add:
        from sqlalchemy.dialects import postgresql
        banner_status = postgresql.ENUM('independent', 'family', name='customertype')
        banner_status.create(op.get_bind())
    """
    INDEPENDENT = "independent"
    FAMILY = "family"


class Customer(Updateable, db.Model):  # type:ignore
    """
    Model for Customers/parents.
    Relation to one user (One-to-one)
    Relation to one, or more Students (One-to-Many).

    Customers can have two types: "Family" or "Independent".
    For the enum change the name in the migration to 'statusstudent' if it doesn't work
    customer_status = postgresql.ENUM('active', 'inactive', name='statusenum')
    customer_status.create(op.get_bind())
    """
    __tablename__ = "customer"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), index=True)
    stripe_id = db.Column(db.String(255), index=True)
    email_lesson_reminder = db.Column(
        db.Boolean(), default=True, server_default='t', nullable=False)
    email_lesson_notes = db.Column(
        db.Boolean(), default=True, server_default='t', nullable=False)
    created_at = db.Column(db.DateTime, default=get_date)
    last_updated = db.Column(
        db.DateTime, default=get_date, onupdate=get_date)
    customer_type = db.Column(
        db.Enum(
            CustomerType,
            values_callable=lambda obj: [e.value for e in obj]
        ),
        nullable=False,
        default=CustomerType.INDEPENDENT.value,
        server_default=CustomerType.INDEPENDENT.value,
        index=True
    )
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

    def __repr__(self):  # pragma: no cover
        return f'<Customer {self.id}>'

    def to_dict(self):
        return {
            "id": self.id,
            "customer_type": self.customer_type.value,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "email": self.user.email,
            'phone': self.user.phone,
            'created_at': self.created_at,
            'last_updated': self.last_updated,
            'last_login': self.user.last_login,
            "email_lesson_reminders": self.email_lesson_reminder,
            "email_lesson_notes": self.email_lesson_notes,
            'students': [i.id for i in (self.students or [])],
            'status': self.status.value,
        }

    @validates("customer_type")
    def validate_customer_type(self, key, customer_type):
        if not isinstance(customer_type, str):
            raise ValueError("invalid customer type")
        if len(customer_type) == 0:
            raise ValueError("invalid customer type")
        if customer_type != 'independent' and customer_type != 'family':
            raise ValueError("invalid customer type")
        return customer_type

    @staticmethod
    def get_customer_by_id(customer_id=int):
        return Customer.query.get(customer_id)

    @staticmethod
    def get_customer_by_email(email):
        customer = User.query.filter_by(email=email).first()
        return customer
            
    @staticmethod
    def update_customer(id, **kwargs):
        """Updates a Customer and their related User Account

        Gets the customer by the customer ID. Not the User ID.

        Returned the updated Customer Object
        """

        # seperate the arguments to the ones related to the User Account and the ones related to the Customer.
        arguments_for_user = {}
        arguments_for_customer = {}
        for key, value in kwargs.items():
            if key in ('first_name', 'last_name', 'phone', 'email'):
                arguments_for_user[key] = value
            else:
                arguments_for_customer[key] = value

        # Update both the customer and user.
        customer = Customer.get_customer_by_id(id)
        User.update(customer.user, arguments_for_user)
        db.session.commit()
        updated_customer = Customer.update(customer, arguments_for_customer)
        db.session.commit()
        print(updated_customer.to_dict())
        return updated_customer

    @staticmethod
    def delete_customer(id=str):
        """ 
        Deletes a customer and their User account from the DB.
        Deletes also all related students and their User accounts.

        ID is the Customer ID.
        """
        # Get the Customer or Abort.
        customer = Customer.query.get(id) or abort(404)

        # Get the Customer User Account.
        user = customer.user

        # If Customer has any students assigned then delete them and their user accounts.
        if customer.students:
            for student in customer.students:
                db.session.delete(student)
                if student.user:
                    db.session.delete(student.user)

        db.session.delete(customer)
        db.session.delete(user)
        db.session.commit()
        return customer

    @staticmethod
    def add_customer_user(email: str, password: str, first_name: str, last_name: str, phone: str, **kwargs):
        """
            Adds a customer with a user account, but without an associated student.
            Use Kwargs to add any customer specific data.
        """
        user = User(email=email, password=password,
                    first_name=first_name, last_name=last_name, phone=phone)
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
            send_email([email], 'Confirm your account', template)
        customer = Customer(user_id=user.uid, **kwargs)
        db.session.add(customer)
        db.session.commit()

        return {"customer": customer, "user": user}

    @staticmethod
    def add_independent_customer_with_student(email: str, password: str,
                                first_name: str, last_name: str, phone: str,
                                student_data: dict = {}, **kwargs):
        """
            Adds an independent customer with a user account and a student.
            Use Kwargs to add any customer specific data.
            Add a dictionary with the student_data argument.

            Returns a dictionary with the Customer Object, User Object, and Student Object.
        """
        user = User(email=email, password=password,
                    first_name=first_name, last_name=last_name, phone=phone)
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
            send_email([email], 'Confirm your account', template)
        customer = Customer(user_id=user.uid, **kwargs)
        db.session.add(customer)
        db.session.commit()

        student = Student(customer_id=customer.id, email=email, first_name=first_name,
                          last_name=last_name, student_type='independent', **student_data)
        db.session.add(student)
        db.session.commit()

        return {"customer": customer, "user": user, "student": student}

    @staticmethod
    def add_student_to_family(email: str, student_data: dict = {}, **kwargs):
        """
            Creates a student and assigns them to a a family.
            Use Kwargs to add any customer specific data.
            Add a dictionary with the student_data argument.
        """

        user = User.query.filter_by(email=email).first() or abort(404)
        student = Student(customer_id=user.customer.id,
                          status=user.customer.status,
                          **student_data)
        db.session.add(student)
        db.session.commit()
        return {"student": student, "user": user}

    @staticmethod
    def convert_to_family_student(**kwargs):
        old_user = User.find_by_email(kwargs['old_email'])
        old_user.customer.customer_type = 'family'
        print(old_user.customer.customer_type)
        customer_account = old_user.customer
        student = old_user.customer.students[0]
        # give student data to the old account
        old_user.email = student.email
        old_user.first_name = student.first_name
        old_user.last_name = student.last_name
        # probably make unverified later because we don't want to let the change not be verified first
        student.user_id = old_user.uid
        # give new family data to student account
        new_user = User(email=kwargs['email'], password=kwargs['password'],
                        first_name=kwargs['first_name'], last_name=kwargs['last_name'], phone=kwargs['phone'])
        db.session.add(new_user)
        db.session.commit()
        print(new_user)
        customer_account.user_id = new_user.uid
        db.session.commit()
        # customer = Customer(user_id=user.uid, **kwargs)
        # db.session.add(customer)
        # db.session.commit()

        # return {"customer":customer,"user":user}
        return new_user

    @staticmethod
    def change_status(email: str, status: str, **kwargs):
        """
            Changes the status of the customer.
            Use Kwargs to add any customer specific data.
            Changes the status for all assigned tutors as well.
        """
        user = User.query.filter_by(email=email).first()
        customer = user.customer

        # If customer has any students assigned then change their status too.
        if customer.students:
            for i in customer.students:
                i.status = status
        customer.status = status
        db.session.merge(user)
        db.session.commit()
        return user

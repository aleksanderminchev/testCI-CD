import unittest
from sqlalchemy import text

from api.app import create_app, db
from models.user import User
from models.customer import Customer
from models.balance import Balance
from models.order import Order
from models.admin import Admin
from models.student import Student
from models.teacher import Teacher
from models.higher_education_institution import HigherEducationInstitution
from models.higher_education_programme import HigherEducationProgramme

from config import Config


class TestConfig(Config):
    SERVER_NAME = 'localhost:5000'
    TESTING = True
    DISABLE_AUTH = True
    ALCHEMICAL_DATABASE_URL = 'sqlite://'
    CONFIG_NAME = 'testing'
    SQLALCHEMY_POOL_SIZE = None
    SQLALCHEMY_MAX_OVERFLOW = None


class TestConfigWithAuth(TestConfig):
    DISABLE_AUTH = False
    REFRESH_TOKEN_IN_BODY = True


class BaseTestCase(unittest.TestCase):
    config = TestConfig

    @classmethod
    def setUpClass(self):
        self.app = create_app(self.config.CONFIG_NAME)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user_teacher = User(email='teacher@test.com', password='foo')
        user = User(email='test@test.dk', password='foo')
        user2 = User(email='test@example.com', password='foo')
        db.session.add(user)
        db.session.add(user_teacher)
        db.session.add(user2)
        db.session.commit()

        customer = Customer(user_id=user.uid, status='active',)
        customer2 = Customer(user_id=user2.uid, status='active',)
        db.session.add(customer)
        db.session.add(customer2)
        db.session.commit()
        self.customer = customer

        teacher = Teacher(user_id=user_teacher.uid, wage_per_hour=120.00, bio="ewfewvwv",
                          photo="wdq", open_for_new_students=True, payroll_id="122222-2311", status='active',)
        db.session.add(teacher)
        db.session.commit()
        student = Student(user_id=user.uid,
                          customer_id=customer.id, status='active',)
        db.session.add(student)
        db.session.commit()

        Admin.add_new_admin(email="admin@mail.com", password="admin")
        higher_edu_inst = HigherEducationInstitution(name="KEA")
        higher_edu_programme = HigherEducationProgramme(name="COMPSCI")
        db.session.add(higher_edu_programme)
        db.session.add(higher_edu_inst)
        db.session.commit()

        self.client = self.app.test_client()

    @classmethod
    def tearDownClass(self):
        print('TEARING DOWN THE HOUSE')
        db.session.close()
        db.drop_all()
        self.app_context.pop()

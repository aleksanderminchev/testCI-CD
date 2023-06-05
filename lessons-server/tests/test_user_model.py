import pytest
from api.app import db
from models.user import User
from models.token import Token
from models.teacher import Teacher
from models.customer import Customer
from models.student import Student

from tests.base_test_case import BaseTestCase


class UserModelTests(BaseTestCase):
    def test_password_hashing(self):
        u = User(email='susan@mail.com', password='cat')
        assert not u.verify_password('dog')
        assert u.verify_password('cat')
        with pytest.raises(AttributeError):
            u.password

    def test_user_creation(self):
        u = User(email='john@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        user = User.query.filter_by(email='john@mail.com').first()
        assert user.email == 'john@mail.com'

    def test_user_exists(self):
        u = User(email='exists@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        assert u.exists('exists@mail.com')

    def test_find_by_email(self):
        u = User(email='find@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()

        found_user = User.find_by_email('find@mail.com')
        assert found_user is not None
        assert found_user.email == 'find@mail.com'
        assert found_user.uid == u.uid

        not_found_user = User.find_by_email('nonexistent@mail.com')
        assert not_found_user is None

    def test_generate_verify_access_refresh_tokens(self):
        u = User(email='verify@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        token = u.generate_auth_token()
        db.session.add(token)
        db.session.commit()

        user = User.verify_access_token(token.access_token)
        assert user.email == 'verify@mail.com'

        refreshed_token = User.verify_refresh_token(
            token.refresh_token, token.access_token)
        assert refreshed_token is not None

    def test_revoke_all_tokens(self):
        u = User(email='revoke@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        token = u.generate_auth_token()
        db.session.add(token)
        db.session.commit()

        u.revoke_all()
        db.session.commit()
        revoked_token = Token.query.filter(Token.user == u).first()
        assert revoked_token is None

    def test_generate_verify_reset_token(self):
        u = User(email='reset@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        reset_token = u.generate_reset_token()
        user = User.verify_reset_token(reset_token)
        assert user.email == 'reset@mail.com'

    def test_to_dict(self):
        u = User(email='dict@mail.com', password='doe',
                 first_name='John', last_name='Doe')
        db.session.add(u)
        db.session.commit()
        user_dict = u.to_dict()
        assert user_dict['email'] == 'dict@mail.com'
        assert user_dict['first_name'] == 'John'
        assert user_dict['last_name'] == 'Doe'

    def test_teacher_relationship(self):
        u = User(email='teacher@mail.com', password='doe')
        t = Teacher(user=u)
        db.session.add(u)
        db.session.add(t)
        db.session.commit()

        teacher = Teacher.query.filter_by(user_id=u.uid).first()
        assert teacher is not None
        assert u.teacher == teacher

    def test_customer_relationship(self):
        u = User(email='customer@mail.com', password='doe')
        c = Customer(user=u)
        db.session.add(u)
        db.session.add(c)
        db.session.commit()

        customer = Customer.query.filter_by(user_id=u.uid).first()
        assert customer is not None
        assert u.customer == customer

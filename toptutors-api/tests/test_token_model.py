from datetime import datetime, timedelta
from api.app import db
from models.token import Token
from models.user import User
from tests.base_test_case import BaseTestCase


class TokenModelTests(BaseTestCase):
    def test_token_generate(self):
        u = User(email='tokenuser@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        user = User.query.filter_by(email='tokenuser@mail.com').first()

        token = Token(user=user)
        token.generate()
        db.session.add(token)
        db.session.commit()

        assert token.access_token is not None
        assert token.refresh_token is not None
        assert token.access_expiration is not None
        assert token.refresh_expiration is not None

    def test_token_expire(self):
        u = User(email='tokenexpire@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        user = User.query.filter_by(email='tokenexpire@mail.com').first()

        token = Token(user=user)
        token.generate()
        db.session.add(token)
        db.session.commit()

        token.expire()
        db.session.commit()

        assert token.access_expiration <= datetime.utcnow()
        assert token.refresh_expiration <= datetime.utcnow()

    def test_token_clean(self):
        u = User(email='tokenclean@mail.com', password='doe')
        db.session.add(u)
        db.session.commit()
        user = User.query.filter_by(email='tokenclean@mail.com').first()

        token1 = Token(
            access_token='a1', refresh_token='r1',
            access_expiration=datetime.utcnow() + timedelta(days=1),
            refresh_expiration=datetime.utcnow() + timedelta(days=1),
            user=user)
        token2 = Token(
            access_token='a2', refresh_token='r2',
            access_expiration=datetime.utcnow() - timedelta(days=2),
            refresh_expiration=datetime.utcnow() - timedelta(days=2),
            user=user)
        db.session.add_all([token1, token2])
        db.session.commit()

        Token.clean()
        db.session.commit()

        tokens = Token.query.all()
        assert len(tokens) == 1
        assert tokens[0].access_token == 'a1'

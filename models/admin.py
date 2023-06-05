from api.app import db
from models.user import User
from api.utils.utils import Updateable


class Admin(Updateable, db.Model):  # type:ignore
    """
    Model for Admins.
    Relation to one user (One-to-One)
    """

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.uid'), index=True)
    # One Admin to One User relation
    user = db.relationship("User", backref="admin", uselist=False)

    @staticmethod
    def add_new_admin(email, password):
        """ Adds a new admin user to the DB. """
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        admin = Admin(user_id=user.uid)
        db.session.add(admin)
        db.session.commit()

        return admin

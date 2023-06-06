from api.app import db
from api.utils.utils import Updateable
from models.user import User
from flask import abort

teachers_interests = db.Table('teacher_interests',
                              db.Column('interest_id', db.Integer, db.ForeignKey(
                                  'interest.uid'), primary_key=True, index=True),
                              db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'),
                                        primary_key=True, index=True))


class Interest(Updateable, db.Model):  # type:ignore

    __tablename__ = "interest"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    teachers = db.relationship("Teacher", secondary=teachers_interests, primaryjoin=(
        teachers_interests.c.interest_id == uid), backref='interests')

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.uid
        }

    def to_tutormap(self):
        return self.name

    @staticmethod
    def get_interest_by_id(id):
        return Interest.query.get(id)

    @staticmethod
    def update_interest(id=int, **kwargs):
        """Updates a interest by the User id from the DB"""
        interest_query = Interest.query.get(id)
        Interest.update(interest_query, kwargs)
        db.session.commit()
        return interest_query

    @staticmethod
    def add_new_interest(**kwargs):
        """ Adds a new interest to the DB. TODO """
        interest = Interest(**kwargs)
        db.session.add(interest)
        db.session.commit()
        return interest.to_dict()

    @staticmethod
    def delete_interest(id=str):
        """Deletes a interest from the DB"""
        interest = Interest.query.get(id) or abort(404)
        db.session.delete(interest)
        db.session.commit()
        return interest

    @staticmethod
    def add_interest_to_teacher(teacher, interest_id):
        interest = Interest.get_interest_by_id(interest_id)
        interests = teacher.interests
        if interest not in interests:
            interests.append(interest)
            db.session.commit()
            return interest

    @staticmethod
    def remove_interest_from_teacher(teacher_email, interest_id):
        teacher_user = User.find_by_email(teacher_email)
        interest = Interest.get_interest_by_id(interest_id)
        interests = teacher_user.teacher.interests
        if interest not in interests:
            abort(500)
        interests.remove(interest)
        db.session.add(teacher_user)
        db.session.commit()
        return interest

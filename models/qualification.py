from api.app import db
from api.utils.utils import Updateable
from models.user import User
from flask import abort


teachers_qualifications = db.Table('teacher_qualifications',
                                   db.Column('qualification_id', db.Integer, db.ForeignKey(
                                       'qualification.uid'), primary_key=True, index=True),
                                   db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'),
                                    primary_key=True, index=True))


class Qualification(Updateable, db.Model):  # type:ignore

    __tablename__ = "qualification"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    teachers = db.relationship("Teacher", secondary=teachers_qualifications, primaryjoin=(
        teachers_qualifications.c.qualification_id == uid), backref='qualifications')

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.uid
        }
    def to_tutormap(self):
        return self.name
        
    @staticmethod
    def get_qualification_by_id(id):
        return Qualification.query.get(id)

    @staticmethod
    def update_qualification(id=int, **kwargs):
        """Updates a qualification by the User id from the DB"""
        qualification_query = Qualification.query.get(id)
        Qualification.update(qualification_query, kwargs)
        db.session.commit()
        return qualification_query

    @staticmethod
    def add_new_qualification(**kwargs):
        """ Adds a new qualification to the DB. TODO """
        qualification = Qualification(**kwargs)
        db.session.add(qualification)
        db.session.commit()
        return qualification.to_dict()

    @staticmethod
    def delete_qualification(id=str):
        """Deletes a qualification from the DB"""
        qualification = Qualification.query.get(id) or abort(404)
        db.session.delete(qualification)
        db.session.commit()
        return qualification

    @staticmethod
    def add_qualification_to_teacher(teacher, qualification_id):
        qualification = Qualification.get_qualification_by_id(qualification_id)
        qualifications = teacher.qualifications
        if qualification not in qualifications:
            qualifications.append(qualification)
            db.session.commit()
            return qualification

    @staticmethod
    def remove_qualification_from_teacher(teacher_email, qualification_id):
        teacher_user = User.find_by_email(teacher_email)
        qualification = Qualification.get_qualification_by_id(qualification_id)
        qualifications = teacher_user.teacher.qualifications
        if qualification not in qualifications:
            abort(500)
        qualifications.remove(qualification)
        db.session.add(teacher_user)
        db.session.commit()
        return qualification

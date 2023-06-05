from api.app import db
from api.utils.utils import Updateable
from flask import abort
from models.user import User


class Subjects(Updateable, db.Model):  # type:ignore

    __tablename__ = "subjects"
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    def to_dict(self):
        return {
            "name": self.name,
            "id": self.uid
        }

    def to_tutormap(self):
        return self.name
        
    @staticmethod
    def add(item):
        subject = Subjects()
        subject.subject = item

        return subject

    @staticmethod
    def return_objects_from_list(subjects_list, session):
        return session.query(Subjects).filter(Subjects.subject.in_(subjects_list)).all()

    @staticmethod
    def get_subject_by_id(id):
        return Subjects.query.get(id)

    @staticmethod
    def update_subject(id=int, **kwargs):
        """Updates a subject by the User id from the DB"""
        subject = Subjects.query.get(id)
        Subjects.update(subject, kwargs)
        db.session.commit()
        return subject

    @staticmethod
    def add_new_subject(**kwargs):
        """ Adds a new subject to the DB. TODO """
        subject = Subjects(**kwargs)
        db.session.add(subject)
        db.session.commit()
        return subject.to_dict()

    @staticmethod
    def delete_subject(id=str):
        """Deletes a subject from the DB"""
        subject = Subjects.query.get(id) or abort(404)
        db.session.delete(subject)
        db.session.commit()
        return subject

    @staticmethod
    def delete(session):
        session.query(Subjects).delete()
        session.commit()

    @staticmethod
    def add_subject_to_teacher(subject_id, teacher):
        subject = Subjects.get_subject_by_id(subject_id)
        subjects = teacher.subjects
        if subject not in subjects:
            subjects.append(subject)
            db.session.commit()
            return subject

    @staticmethod
    def remove_subject_from_teacher(subject_id, teacher_email):
        teacher_user = User.find_by_email(teacher_email)
        subject = Subjects.get_subject_by_id(subject_id)
        subjects = teacher_user.teacher.subjects
        if subject not in subjects:
            abort(500)
        subjects.remove(subject)
        db.session.add(teacher_user)
        db.session.commit()
        return subject

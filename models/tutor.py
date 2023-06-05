from api.app import db
from datetime import datetime as dt
from . import relationships


class Tutor(db.Model):  # type:ignore

    __table__name__ = "Tutor"

    uid = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    bio = db.Column(db.String, nullable=True)
    grade_average = db.Column(db.String, nullable=True)
    age = db.Column(db.Integer, nullable=True)
    age_interval = db.Column(db.String, nullable=True)
    subjects = db.Column(db.String, nullable=True)
    subjects_relationship = db.relationship(
        "Subjects", secondary=relationships.tutor_subject, backref="tutors_subject")
    photo = db.Column(db.String, nullable=True)
    status = db.Column(db.String, nullable=True)
    marketing_consent = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, nullable=True)
    # courses = db.relationship("Course", backref="tutor")

    @staticmethod
    def add_new(data, session=None):
        tutor = Tutor()
        tutor.tutor_id = data["id"]
        tutor.name = f'{data["first_name"]} {data["last_name"]}'
        tutor.email = data["email"]
        tutor.phone = data["mobile_phone"]
        tutor.bio = data["bio"]
        tutor.subjects = data["formatted_subjects"]
        tutor.photo = data["photo"]
        tutor.status = data["status"]
        tutor.updated_at = data["updated_at"]
        tutor.grade_average = data["grade"]
        tutor.age_interval = data["age_interval"]
        tutor.age = data["age"]

        return tutor

    @staticmethod
    def update(tutor, data):
        tutor.name = f'{data["first_name"]} {data["last_name"]}'
        tutor.email = data["email"]
        tutor.phone = data["mobile_phone"]
        tutor.bio = data["bio"]
        tutor.subjects = data["subjects"]
        tutor.updated_at = dt.strptime(
            data["updated_at"], "%Y-%m-%dT%H:%M:%S.000Z")
        tutor.grade_average = data["grade"]
        tutor.age_interval = data["age_interval"]
        tutor.age = data["age"]

    def in_db(self, session):
        return bool(session.query(Tutor).filter_by(tutor_id=self.tutor_id).first())

    @staticmethod
    def get_tutor_by_tw_id(tw_id):
        """ Gets tutor by tw_id"""
        return Tutor.query.filter_by(tutor_id=tw_id).first()

    @staticmethod
    def get_tutor_by_uid(uid):
        """ Gets tutor by tw_id"""
        return Tutor.query.filter_by(uid=uid).first()

    @staticmethod
    def get_from_kwarg(session, **data):
        """
        The key needs to match the field name in the Tutor model.
        """
        query = session.query(Tutor).filter_by(**data).first()
        if bool(query):
            return query
        return None

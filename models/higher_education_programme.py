from api.app import db
from api.utils.utils import Updateable
from models.student import User
from flask import abort

teachers_programmes = db.Table('teacher_programme',
                               db.Column('higher_education_programme_id', db.Integer, db.ForeignKey(
                                   'higher_education_programme.id'), primary_key=True, index=True),
                               db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True, index=True))


class HigherEducationProgramme(Updateable, db.Model):  # type:ignore

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    teachers = db.relationship("Teacher", secondary=teachers_programmes, primaryjoin=(
        teachers_programmes.c.higher_education_programme_id == id), backref='higher_education_programmes')
    
    def to_tutormap(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @staticmethod
    def add_higher_edu_programme_to_teacher(higher_edu_programme_id, teacher):
        higher_edu_programme = HigherEducationProgramme.query.get(
            higher_edu_programme_id)
        higher_edu_programmes = teacher.higher_education_programmes
        if higher_edu_programme not in higher_edu_programmes:
            higher_edu_programmes.append(higher_edu_programme)
            db.session.commit()
            return higher_edu_programme

    @staticmethod
    def remove_higher_edu_programme_from_teacher(higher_edu_programme_id, teacher_email):
        teacher_user = User.find_by_email(teacher_email)
        higher_edu_programme = HigherEducationProgramme.query.get(
            higher_edu_programme_id)
        higher_edu_programmes = teacher_user.teacher.higher_education_programmes
        if higher_edu_programme not in higher_edu_programmes:
            abort(500)
        higher_edu_programmes.remove(higher_edu_programme)
        db.session.add(teacher_user)
        db.session.commit()
        return higher_edu_programme

from api.app import db
from api.utils.utils import Updateable
from models.student import User
from flask import abort

teachers_institutions = db.Table('teacher_institution',
                                 db.Column('higher_education_institution_id', db.Integer, db.ForeignKey(
                                     'higher_education_institution.id'), primary_key=True, index=True),
                                 db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True, index=True))


class HigherEducationInstitution(Updateable, db.Model):  # type:ignore
    """ Class for the options of higher education institutions. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    teachers = db.relationship("Teacher", secondary=teachers_institutions, primaryjoin=(
        teachers_institutions.c.higher_education_institution_id == id), backref='higher_education_institutions')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def to_tutormap(self):
        return self.name

    @staticmethod
    def add_higher_edu_institution_to_teacher(higher_edu_institution_id, teacher):
        """ Adds 1 higher educational institition relation to a teacher. """
        higher_edu_institution = HigherEducationInstitution.query.get(
            higher_edu_institution_id)
        higher_edu_institutions = teacher.higher_education_institutions
        if higher_edu_institution not in higher_edu_institutions:
            higher_edu_institutions.append(higher_edu_institution)
            db.session.commit()
            return higher_edu_institution

    @staticmethod
    def remove_higher_edu_institution_from_teacher(higher_edu_institution_id, teacher_email):
        teacher_user = User.find_by_email(teacher_email)
        higher_edu_institution = HigherEducationInstitution.query.get(
            higher_edu_institution_id)
        higher_edu_institutions = teacher_user.teacher.higher_education_institutions
        if higher_edu_institution not in higher_edu_institutions:
            abort(500)
        higher_edu_institutions.remove(higher_edu_institution)
        db.session.add(teacher_user)
        db.session.commit()
        return higher_edu_institution

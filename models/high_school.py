from api.app import db
from api.utils.utils import Updateable
from models.student import User
from flask import abort

teachers_highschool = db.Table('teacher_highschool',
                               db.Column('high_school_id', db.Integer, db.ForeignKey(
                                   'high_school.id'), primary_key=True, index=True),
                               db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True, index=True))


class HighSchool(Updateable, db.Model):  # type:ignore

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    teachers = db.relationship("Teacher", secondary=teachers_highschool, primaryjoin=(
        teachers_highschool.c.high_school_id == id), backref='high_school')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def to_tutormap(self):
        return self.name

    @staticmethod
    def add_high_school_to_teacher(high_school_id, teacher):
        high_school = HighSchool.query.get(high_school_id)
        high_schools = teacher.high_school
        if high_school not in high_schools:
            high_schools.append(high_school)
            db.session.commit()
            return high_school

    @staticmethod
    def remove_high_school_from_teacher(high_school_id, teacher_email):
        teacher_user = User.find_by_email(teacher_email)
        high_school = HighSchool.query.get(high_school_id)
        high_schools = teacher_user.teacher.high_school
        if high_school not in high_schools:
            abort(500)
        high_schools.remove(high_school)
        db.session.add(teacher_user)
        db.session.commit()
        return high_school

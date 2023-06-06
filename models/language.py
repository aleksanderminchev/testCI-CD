from api.app import db
from api.utils.utils import Updateable
from models.user import User
from flask import abort


teachers_languages = db.Table('teacher_languages',
                              db.Column('language_id', db.Integer, db.ForeignKey(
                                  'language.uid'), primary_key=True),
                              db.Column('teacher_id', db.Integer, db.ForeignKey('teacher.id'), primary_key=True))


class Language(Updateable, db.Model):  # type:ignore

    __tablename__ = "language"
    uid = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String)
    teachers = db.relationship("Teacher", secondary=teachers_languages, primaryjoin=(
        teachers_languages.c.language_id == uid), backref='languages')

    def to_dict(self):
        return {
            "name": self.name,
            "id": self.uid
        }

    def to_tutormap(self):
        return self.name

    @staticmethod
    def get_language_by_id(id):
        return Language.query.get(id)

    @staticmethod
    def update_language(id=int, **kwargs):
        """Updates a language by the User id from the DB"""
        language_query = Language.query.get(id)
        Language.update(language_query, kwargs)
        db.session.commit()
        return language_query

    @staticmethod
    def add_new_language(**kwargs):
        """ Adds a new language to the DB. """
        language = Language(**kwargs)
        db.session.add(language)
        db.session.commit()
        return language.to_dict()

    @staticmethod
    def delete_language(id=str):
        """Deletes a language from the DB"""
        language = Language.query.get(id) or abort(404)
        db.session.delete(language)
        db.session.commit()
        return language

    @staticmethod
    def add_language_to_teacher(teacher, language_id):
        language = Language.get_language_by_id(language_id)
        languages = teacher.languages
        if language not in languages:
            languages.append(language)
            db.session.commit()
            return language

    @staticmethod
    def remove_language_from_teacher(teacher_email, language_id):
        teacher_user = User.find_by_email(teacher_email)
        language = Language.get_language_by_id(language_id)
        languages = teacher_user.teacher.languages
        if language not in languages:
            abort(500)
        languages.remove(language)
        db.session.add(teacher_user)
        db.session.commit()
        return language

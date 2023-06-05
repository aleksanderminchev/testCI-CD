import pytest
from api.app import db
from api.utils.utils import datetime
from tests.base_test_case import BaseTestCase
from models.language import Language
from models.teacher import Teacher


class LanguageModelTestCase(BaseTestCase):
    def test_add_language_to_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        language = Language(name="English")
        db.session.add(language)
        db.session.commit()
        language.add_language_to_teacher(teacher, language.uid)

        assert language in teacher.languages
        assert len(teacher.languages) != 0
        assert teacher.languages[0].name == 'English'

    def test_remove_language_from_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        language = Language(name="English")
        teacher.languages.append(language)
        db.session.add(language)
        db.session.add(language)
        db.session.commit()
        language.remove_language_from_teacher(
            teacher_email=teacher.user.email, language_id=language.uid)

        assert language not in teacher.languages
        assert len(teacher.languages) == 1

    def test_get_language_by_id(self):
        new_language = Language.add_new_language(name="Spanish")
        found_language = Language.get_language_by_id(new_language["id"])

        assert found_language is not None
        assert found_language.language == "Spanish"

    def test_delete_language(self):
        new_language = Language.add_new_language(name="Polish")
        deleted_language = Language.delete_language(new_language["id"])

        assert new_language["id"] == deleted_language.uid
        assert Language.get_language_by_id(new_language["id"]) is None

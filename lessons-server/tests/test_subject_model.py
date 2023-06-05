from api.app import db
from api.utils.utils import datetime
from tests.base_test_case import BaseTestCase
from models.subjects import Subjects
from models.teacher import Teacher


class SubjectModelTestCase(BaseTestCase):
    def test_add_subject_to_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        subject = Subjects(name="Mathematics")
        db.session.add(subject)
        db.session.commit()
        subject_added = subject.add_subject_to_teacher(subject.uid,teacher)

        assert subject in teacher.subjects
        assert len(teacher.subjects) != 0
        assert teacher.subjects[0].name == 'Mathematics'

    def test_remove_subject_to_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        subject = Subjects(name="Mathematics")
        teacher.subjects.append(subject)
        db.session.add(subject)
        db.session.add(subject)
        db.session.commit()
        subject_added = subject.remove_subject_from_teacher(
            teacher_email=teacher.user.email, subject_id=subject.uid)

        assert subject not in teacher.subjects
        assert len(teacher.subjects) == 1

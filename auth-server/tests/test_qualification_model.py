from api.app import db
from api.utils.utils import datetime
from tests.base_test_case import BaseTestCase
from models.qualification import Qualification
from models.teacher import Teacher


class QualificationModelTestCase(BaseTestCase):
    def test_add_qualification_to_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        qualification = Qualification(
            name="Teaching to students with ADHD")
        db.session.add(qualification)
        db.session.commit()
        qualification_added = qualification.add_qualification_to_teacher( teacher, qualification.uid)

        assert qualification in teacher.qualifications
        assert len(teacher.qualifications) != 0
        assert teacher.qualifications[0].name == 'Teaching to students with ADHD'

    def test_remove_qualification_to_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        qualification = Qualification(
            name="Teaching to students with ADHD")
        teacher.qualifications.append(qualification)
        db.session.add(qualification)
        db.session.add(qualification)
        db.session.commit()
        qualification_added = qualification.remove_qualification_from_teacher(
            teacher_email=teacher.user.email, qualification_id=qualification.uid)

        assert qualification not in teacher.qualifications
        assert len(teacher.qualifications) == 1

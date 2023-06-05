from api.app import db
from tests.base_test_case import BaseTestCase
from models.interest import Interest
from models.teacher import Teacher


class InterestModelTestCase(BaseTestCase):
    def test_add_interest_to_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        interest = Interest(name="Computer games")
        db.session.add(interest)
        db.session.commit()
        interest_added = interest.add_interest_to_teacher(teacher, interest.uid)

        assert interest in teacher.interests
        assert len(teacher.interests) != 0
        assert teacher.interests[0].interest == 'Computer games'

    def test_remove_interest_from_teacher(self):
        teacher = Teacher.get_teacher_by_id(1)
        interest = Interest(name="Computer games")
        teacher.interests.append(interest)
        db.session.add(interest)
        db.session.commit()
        interest_added = interest.remove_interest_from_teacher(
            teacher_email=teacher.user.email, interest_id=interest.uid)

        assert interest not in teacher.interests
        assert len(teacher.interests) == 1

    def test_create_interest(self):
        interest_data = {'name': 'Computer games'}
        interest = Interest.add_new_interest(**interest_data)

        assert interest is not None
        assert interest["name"] == "Computer games"

    def test_update_interest(self):
        interest_data = {'name': 'Badminton'}
        interest = Interest.add_new_interest(**interest_data)
        updated_interest = Interest.update_interest(
            interest["id"], interest='Reading')

        assert interest is not None
        assert interest["name"] == "Badminton"

        assert updated_interest is not None
        assert updated_interest.interest == "Reading"

    def test_delete_interest(self):
        interest_data = {'name': 'Fishing'}
        interest = Interest.add_new_interest(**interest_data)

        assert interest is not None
        assert interest["name"] == "Fishing"

        Interest.delete_interest(interest["id"])

        assert Interest.get_interest_by_id(interest["id"]) is None

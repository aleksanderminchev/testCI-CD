from tests.base_test_case import BaseTestCase



class CourseModelTests(BaseTestCase):
    def test_create_course(self):
        # Create a user with required information:
        rv = self.client.post('/api/courses/generate_course_url', json={
            'name': 'Mikkel Christensen',
            'hours_per_session': 4,
            'crm_deal_id': 123,
            'weekly_frequency': 2,
            'estimated_length': "resten af skoleåret",
            "course_type": "Generel undervisning (Privatundervisning og lektiehjælp)",
            "subjects": "Matematik B"
        })

        assert rv.status_code == 201
        # Create a user with all information:
        rv = self.client.post('/api/courses/generate_course_url', json={
            "subjects": "Dansk C, Matematik C",
            "crm_deal_id": 1234,
            "course_type": "Generel undervisning (Privatundervisning og lektiehjælp)",
            "name": "Dorde Hansen",
            "hours_per_session": 8,
            "weekly_frequency": 4,
            "estimated_length": "resten af skoleåret",
            "class_grade": "1.g",
            "education": "STX",
            "math_programs": "Maple",
            "comment": "Dygtig",
            "unavailable_days": "Onsdag",
            "hidden": True,
            "status": "Pending"
        })
        assert rv.status_code == 201

    def update_course(self):
        rv = self.client.post('/api/courses/generate_course_url', json={
            'name': 'Mikkel Christensen',
            'hours_per_session': 4,
            'crm_deal_id': 123,
            'weekly_frequency': 2,
            'estimated_length': "resten af skoleåret",
            "course_type": "Generel undervisning (Privatundervisning og lektiehjælp)",
            "subjects": "Matematik B"
        })




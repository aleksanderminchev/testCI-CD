import pytest
from apifairy.exceptions import ValidationError

from tests.base_test_case import BaseTestCase


class UserTests(BaseTestCase):
    def test_create_user(self):
        # Create a user with all information
        rv = self.client.post('/api/users', json={
            'first_name': 'Mikkel',
            'last_name': 'Christensen',
            'email': 'mikkel@example.com',
            'password': 'dog',
            'phone': "+4523961972"
        })
        assert rv.status_code == 201

        # Creating a user with only the required information
        rv = self.client.post('/api/users', json={
            'email': 'christian@example.com',
            'password': 'dog'
        })
        assert rv.status_code == 201

    def test_create_invalid_user(self):
        # Create a user with an invalid password: less than 3 characters
        with pytest.raises(ValidationError, match=r".*Shorter than minimum length 3.*"):
            self.client.post('/api/users', json={
                'email': 'invalid@example.com',
                'password': '12'
            })

        # Create a user with invalid email: Email aldready exists
        rv = self.client.post('/api/users', json={
            'email': 'exists@example.com',
            'password': 'dog',
        })
        assert rv.status_code == 201
        with pytest.raises(ValidationError, match=r".*Email already exists.*"):
            self.client.post('/api/users', json={
                'email': 'exists@example.com',
                'password': 'dog2',
            })

        # Create a user with invalid email: Email is too long
        with pytest.raises(ValidationError, match=r".*Longer than maximum length 120.*"):
            self.client.post('/api/users', json={
                'email': 'christianchristianchristianchristianchristianchristianchristianchristianchristianchristianchristianchristianchristianchristianchristian@example.com',
                'password': 'dog2',
            })

        # Create a user with invalid email: It is not an email
        with pytest.raises(ValidationError, match=r".*Not a valid email address.*"):
            self.client.post('/api/users', json={
                'email': 'christian.com',
                'password': 'dog2',
            })
        with pytest.raises(ValidationError, match=r".*Not a valid email address.*"):
            self.client.post('/api/users', json={
                'email': 'christian@.com',
                'password': 'dog2',
            })
        with pytest.raises(ValidationError, match=r".*Not a valid email address.*"):
            self.client.post('/api/users', json={
                'email': '@gmail.com',
                'password': 'dog2',
            })
        with pytest.raises(ValidationError, match=r".*Not a valid email address.*"):
            self.client.post('/api/users', json={
                'email': 'gmail.com',
                'password': 'dog2',
            })
        with pytest.raises(ValidationError, match=r".*Not a valid email address.*"):
            rv = self.client.post('/api/users', json={
                'email': 'gmail',
                'password': 'dog2',
            })

        # create a user with invalid phone number without country code.
        with pytest.raises(ValidationError, match=r".*String does not match expected pattern.*"):
            self.client.post('/api/users', json={
                'email': 'christian2@example.com',
                'password': 'dog',
                'phone': "23961972"
            })

    def test_get_user_by_id(self):
        # Create a user
        rv = self.client.post('/api/users', json={
            'email': 'testuser@example.com',
            'password': 'password'
        })
        assert rv.status_code == 201

        # Get the user by ID
        user_id = rv.json['uid']
        # authenication
        rv = self.client.post(
            '/api/tokens', auth=('testuser@example.com', 'password'))
        assert rv.status_code == 200
        access_token = rv.json['access_token']

        rv = self.client.get(f'/api/users/{user_id}', headers={
            'Authorization': f'Bearer {access_token}'})
        assert rv.status_code == 200
        assert rv.json['uid'] == user_id
        assert rv.json['email'] == 'testuser@example.com'
        assert 'password' not in rv.json

    def test_get_user_by_email(self):
        # Create a user
        rv = self.client.post('/api/users', json={
            'email': 'testmail@example.com',
            'password': 'password'
        })
        assert rv.status_code == 201

        # authenication
        rv = self.client.post(
            '/api/tokens', auth=('testmail@example.com', 'password'))
        assert rv.status_code == 200
        access_token = rv.json['access_token']

        # Get the user by email
        rv = self.client.get('/api/users/testmail@example.com', headers={
            'Authorization': f'Bearer {access_token}'})
        assert rv.status_code == 200
        assert rv.json['email'] == 'testmail@example.com'
        assert 'password' not in rv.json

    def test_update_user(self):
        # Create a user
        rv = self.client.post('/api/users', json={
            'email': 'updateuser@example.com',
            'password': 'password'
        })
        assert rv.status_code == 201

        # Get an access token
        rv = self.client.post(
            '/api/tokens', auth=('updateuser@example.com', 'password'))
        assert rv.status_code == 200
        access_token = rv.json['access_token']

        # Update the user's information
        rv = self.client.put('/api/me', headers={'Authorization': f'Bearer {access_token}'}, json={
            'first_name': 'Updated',
            'last_name': 'User'
        })
        assert rv.status_code == 200
        assert rv.json['first_name'] == 'Updated'
        assert rv.json['last_name'] == 'User'
        assert 'password' not in rv.json

    def test_get_non_existent_user(self):
        # Try to get a non-existent user by ID
        rv = self.client.get('/api/users/9999')
        assert rv.status_code == 401

    def test_create_user_invalid_first_name(self):
        # Create a user with an invalid first name: shorter than 2 characters
        with pytest.raises(ValidationError, match=r".*Length must be between 2 and 120.*"):
            self.client.post('/api/users', json={
                'first_name': 'A',
                'email': 'invalid@example.com',
                'password': 'password'
            })

        # Create a user with an invalid first name: longer than 120 characters
        with pytest.raises(ValidationError, match=r".*Length must be between 2 and 120.*"):
            self.client.post('/api/users', json={
                'first_name': 'A' * 121,
                'email': 'invalid@example.com',
                'password': 'password'
            })

    def test_create_user_invalid_last_name(self):
        # Create a user with an invalid last name: shorter than 2 characters
        with pytest.raises(ValidationError, match=r".*Length must be between 2 and 120.*"):
            self.client.post('/api/users', json={
                'last_name': 'B',
                'email': 'invalid@example.com',
                'password': 'password'
            })

        # Create a user with an invalid last name: longer than 120 characters
        with pytest.raises(ValidationError, match=r".*Length must be between 2 and 120.*"):
            self.client.post('/api/users', json={
                'last_name': 'B' * 121,
                'email': 'invalid@example.com',
                'password': 'password'
            })

    def test_create_user_invalid_phone(self):
        # Create a user with an invalid phone number: shorter than 6 characters
        with pytest.raises(ValidationError, match=r".*String does not match expected pattern.*"):
            self.client.post('/api/users', json={
                'email': 'invalid@example.com',
                'password': 'password',
                'phone': '+45123'
            })

        # Create a user with an invalid phone number: longer than 16 characters
        with pytest.raises(ValidationError, match=r".*String does not match expected pattern.*"):
            self.client.post('/api/users', json={
                'email': 'invalid@example.com',
                'password': 'password',
                'phone': '+451234567890123456'
            })

        # Create a user with an invalid phone number: String does not match expected pattern
        with pytest.raises(ValidationError, match=r".*String does not match expected pattern.*"):
            self.client.post('/api/users', json={
                'email': 'invalid@example.com',
                'password': 'password',
                'phone': 'not a phone number'
            })

        # Create a user with an invalid phone number: String does not match expected pattern
        with pytest.raises(ValidationError, match=r".*String does not match expected pattern.*"):
            self.client.post('/api/users', json={
                'email': 'invalid@example.com',
                'password': '12345678',
                'phone': '23961972'
            })

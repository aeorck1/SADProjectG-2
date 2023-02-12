from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('UserManagementEndpoints:create')
CREATE_MANAGER_URL = reverse('UserManagementEndpoints:createmanager')
GET_AUTH_TOKEN_URL = reverse('UserManagementEndpoints:authenticate')
USER_URL = reverse('UserManagementEndpoints:me')


def create_user(type="standard", **kwargs):
    model = get_user_model()
    if type == "admin":
        creator_u = model.objects.create_superuser
    elif type == "manager":
        creator_u = model.objects.create_manager
    else:
        creator_u = model.objects.create_user
    user = creator_u(**kwargs)
    return user


class PublicUserApiTests(TestCase):
    """Test for public users"""

    def setUp(self):
        """Initial setups for the tests"""

        self.client = APIClient()
    
    def test_user_creation_endpoint(self):
        """Test for the standard user creation endpoint"""

        data = {
            'email': 'test@email.com',
            'password': 'password9999',
            'name': 'Test Name',
            'department': 'Test Department',
        }

        response = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', response.data)

    def test_existing_user_creation_attempt(self):
        """Test for attempt to create an existing user"""

        data = {
            'email': "test@email.com",
            'password': "testpaswword",
            'name': "Test Name"
        }

        create_user(**data)

        response = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_strong_password(self):
        """Test for strong password"""

        data = {
            'email': "test@email.com",
            'password': "123"
        }

        response = self.client.post(CREATE_USER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=data['email'])

        self.assertFalse(user_exists)
    
    def test_manager_creation(self):
        """Test for creating manager user"""

        data = {
            'email': 'test@email.com',
            'password': 'password9999',
            'name': 'Test Name',
            'department': 'Test Department',
        }

        response = self.client.post(CREATE_MANAGER_URL, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(data['password']))
        self.assertTrue(user.is_staff)
        self.assertNotIn('password', response.data)
    
    def test_user_authetication_token(self):
        """Test for user authentication token"""

        data = {
            'email': 'test@email.com',
            'password': 'testpassword'
        }

        create_user(**data)

        response = self.client.post(GET_AUTH_TOKEN_URL, data)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_invalid_credentials(self):
        """Test of user authentication token creation on invalid credential"""

        create_user(email='test@email.com', password='password999')

        data = {
            'email': 'test@email.com',
            'password': 'wrongpassword'
        }

        response = self.client.post(GET_AUTH_TOKEN_URL, data)
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_existing_auth_token(self):
        """Test for fetching existing auth token for a user"""

        data = {
            'email': 'test@email.com',
            'password': 'testpassword'
        }

        create_user(**data)

        response = self.client.post(GET_AUTH_TOKEN_URL, data)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(GET_AUTH_TOKEN_URL, data)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_user(self):
        """Test for retrieving user as an unathorised user"""

        response = self.client.get(USER_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests for authenticated user"""

    def setUp(self):
        self.user = create_user(
            email='test@email.com',
            password='testpassword',
            name='Test Name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
    
    def test_retrieve_user_data(self):
        """Test for retriving user data"""

        response = self.client.get(USER_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'email': self.user.email,
            'name': self.user.name,
            'department': self.user.department,
        })
    
    def test_post_request_on_endpoint(self):
        """Test for post request on the endpoint"""

        response = self.client.post(USER_URL, {})

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_user_data_update(self):
        """Test for user data update"""

        data = {
            'name': 'Update Name',
            'password': 'newPassword'
        }

        response = self.client.patch(USER_URL, data)

        self.user.refresh_from_db()

        self.assertEqual(self.user.name, data['name'])
        self.assertTrue(self.user.check_password(data['password']))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    # def test_user_update_last_login(self):
    #     """Test for update on last_login"""

    #     import datetime

    #     data = {
    #         'last_login': datetime.datetime.now()
    #     }

    #     response = self.client.patch(USER_URL, data)

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
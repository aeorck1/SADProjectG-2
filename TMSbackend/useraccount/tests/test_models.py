from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def setUp(self):
        """Some test set ups"""

        self.email = "test@email.com"
        self.upperEmail = "test@EMAIL.com"
        self.password = "password999"

    def test_create_user_with_email(self):
        """Test for creating a new user with an email"""

        user = get_user_model().objects.create_user(
            email=self.email,
            password=self.password
        )

        self.assertEqual(user.email, self.email)
        self.assertTrue(user.check_password(self.password))

    def test_email_normalization(self):
        """Test for the normalization of email"""


        user = get_user_model().objects.create_user(self.upperEmail, self.password)

        self.assertEqual(user.email, self.upperEmail.lower())
    
    def test_valid_email(self):
        """Test for user creation with valid email"""

        with self.assertRaises(ValueError):
            user = get_user_model().objects.create_user("", self.password)
    
    def test_create_superuser(self):
        """Test for creating a new superuser"""

        user = get_user_model().objects.create_superuser(self.email, self.password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_manager(self):
        """Test for creating a new manager user"""

        user = get_user_model().objects.create_manager(self.email, self.password)
        self.assertTrue(user.is_staff)
        self.assertFalse(user.is_superuser)

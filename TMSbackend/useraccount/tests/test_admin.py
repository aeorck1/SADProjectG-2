from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

class AdminPageTests(TestCase):
    """Test cases for the admin page"""

    def setUp(self):
        self.client = Client()

        self.admin_user = get_user_model().objects\
            .create_superuser("test@adminemail.com", "password999")

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects\
            .create_user("test@email.com", "password999", name="testname")
        
    def test_user_listing(self):
        """Test for listing all created users on the admin page"""

        url = reverse('admin:useraccount_user_changelist')

        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)
    
    def test_admin_change_page(self):
        """Test Admin change page for user models"""

        url = reverse('admin:useraccount_user_change', args=(self.user.id,))

        response = self.client.get(url)

        self.assertAlmostEqual(response.status_code, 200)
    
    def test_create_user_page(self):
        """Test for the create user page"""
        url = reverse("admin:useraccount_user_add")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
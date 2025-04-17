import unittest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpViewTest(TestCase):  # Abstract class for shared signup tests
    def setUp(self):
        if self.__class__ == SignUpViewTest:
            raise unittest.SkipTest("Abstract SignUpViewTest class - not intended for direct execution")
        self.client = Client()

    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_signup_post_valid(self):
        form_data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'securepass', 'password2': 'securepass'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.profile_create_url)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='new_user')
        self.assertEqual(user.user_type, self.user_type)
        self.assertTrue(user.is_authenticated)

    def test_signup_post_invalid(self):
        form_data = {'username': 'bad_user', 'email': 'bad@example.com', 'password': 'short', 'password2': 'short'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context['form'], self.form_class)
        self.assertIn('password1', response.context['form'].errors)  # Changed 'password' to 'password1'
        self.assertIn('password2', response.context['form'].errors)  # Added assertion for 'password2'
        self.assertEqual(User.objects.count(), 0)

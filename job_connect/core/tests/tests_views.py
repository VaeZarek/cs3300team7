import unittest
from django.contrib.auth.models import Group
from django.test import TestCase, Client
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login
from recruiter.models import RecruiterProfile
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm
from core.urls import urlpatterns


User = get_user_model()


class AuthenticationViewTest(TestCase):  # Renamed for clarity

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('core:login')  # Replace 'login' with your actual login URL name

    def test_valid_login(self):
        # Simulate a POST request to your login view (if applicable)
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, form_data)  # Assuming you have a login view

        # OR, test authenticate and login directly:
        authenticated_user = authenticate(username='testuser', password='testpassword')
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)  # Ensure it's the correct user

        # Simulate a request (if testing login directly)
        self.client.login(username='testuser', password='testpassword')  # A more direct way to login in tests
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertTrue(self.client.session['_auth_user_backend'])

    def test_invalid_username(self):
        authenticated_user = authenticate(username='wronguser', password='testpassword')
        self.assertIsNone(authenticated_user)

    def test_invalid_password(self):
        authenticated_user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(authenticated_user)

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

class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('core:login')
        self.logout_url = reverse('core:logout')
        self.applicant = get_user_model().objects.create_user(
            username='test_applicant', password='testpass', user_type='applicant'
        )
        self.recruiter = get_user_model().objects.create_user(
            username='test_recruiter', password='testpass', user_type='recruiter'
        )
        # Create the RecruiterProfile here:
        RecruiterProfile.objects.create(user=self.recruiter)  # Assuming 'RecruiterProfile' model exists
        self.applicant_dashboard_url = reverse('applicant:applicant_dashboard')
        self.recruiter_dashboard_url = reverse('recruiter:recruiter_dashboard')
        self.home_url = reverse('core:home')

    def test_login_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_post_valid_applicant(self):
        form_data = {'username': 'test_applicant', 'password': 'testpass'}
        response = self.client.post(self.login_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.applicant_dashboard_url)
        logged_in = self.client.login(username='test_applicant', password='testpass')
        self.assertTrue(logged_in)
        self.assertTrue(self.client.session['_auth_user_id'])
        response = self.client.get(self.applicant_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_valid_recruiter(self):
        form_data = {'username': 'test_recruiter', 'password': 'testpass'}
        response = self.client.post(self.login_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.recruiter_dashboard_url)
        logged_in = self.client.login(username='test_recruiter', password='testpass')
        self.assertTrue(logged_in)
        self.assertTrue(self.client.session['_auth_user_id'])
        response = self.client.get(self.recruiter_dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_invalid_credentials(self):
        form_data = {'username': 'test_applicant', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIn('Please enter a correct username and password.', str(response.content))
        self.assertFalse(self.client.session.get('_auth_user_id'))


class LogoutViewTest(TestCase):
    def setUp(self):
        self.logout_url = reverse('core:logout')
        self.home_url = reverse('core:home')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword') # Log in the client

    def test_logout_get(self):
        response = self.client.get(self.logout_url, follow=True) # Follow the redirect
        self.assertEqual(response.status_code, 200) # Expect a 200 on the redirected page (home)
        self.assertFalse(response.wsgi_request.user.is_authenticated) # User should be logged out
        self.assertEqual(response.wsgi_request.path, self.home_url) # Should be redirected to home

    def test_logout_post(self):
        response = self.client.post(self.logout_url, follow=True) # Follow the redirect
        self.assertEqual(response.status_code, 200) # Expect a 200 on the redirected page (home)
        self.assertFalse(response.wsgi_request.user.is_authenticated) # User should be logged out
        self.assertEqual(response.wsgi_request.path, self.home_url) # Should be redirected to home

class ApplicantSignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Applicant')

    def setUp(self):
        self.signup_url = reverse('core:applicant_signup')
        self.profile_create_url = reverse('applicant:applicant_profile_create')
        self.template_name = 'core/applicant_signup.html'
        self.form_class = ApplicantSignUpForm
        self.user_type = 'applicant'

    def test_signup_post_valid(self):
        form_data = {
            'username': 'testapplicant',
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.signup_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, self.profile_create_url)  # Assert the final path
        self.assertTrue(User.objects.filter(username='testapplicant').exists())
        created_user = User.objects.get(username='testapplicant')
        self.assertTrue(created_user.groups.filter(name='Applicant').exists())

class RecruiterSignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Recruiter')

    def setUp(self):
        self.signup_url = reverse('core:recruiter_signup')
        self.profile_create_url = reverse('recruiter:recruiter_profile_create')
        self.template_name = 'core/recruiter_signup.html'
        self.form_class = RecruiterSignUpForm
        self.user_type = 'recruiter'

    def test_signup_post_valid(self):
        form_data = {
            'username': 'testrecruiter',
            'email': 'recruiter@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        response = self.client.post(self.signup_url, form_data, follow=True)
        self.assertRedirects(response, self.profile_create_url)
        self.assertTrue(User.objects.filter(username='testrecruiter').exists())
        created_user = User.objects.get(username='testrecruiter')
        self.assertTrue(created_user.groups.filter(name='Recruiter').exists())

class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view_get(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

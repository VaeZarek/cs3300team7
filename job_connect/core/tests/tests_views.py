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


class AuthenticationViewTest(TestCase):  # :no-index:  Renamed for clarity
    """
    Tests for the authentication views (login, signup, logout).
    """

    def setUp(self):
        """
        Set up test data for authentication tests.
        """

        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('core:login')  # :no-index:  Replace 'login' with your actual login URL name

    def test_valid_login(self):
        """
        Test that a user can log in with valid credentials.
        """

        # :no-index: Simulate a POST request to your login view (if applicable)
        form_data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, form_data)  # :no-index: Assuming you have a login view

        # :no-index: OR, test authenticate and login directly:
        authenticated_user = authenticate(username='testuser', password='testpassword')
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user, self.user)  # :no-index: Ensure it's the correct user

        # :no-index: Simulate a request (if testing login directly)
        self.client.login(username='testuser', password='testpassword')  # :no-index: A more direct way to login in tests
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertTrue(self.client.session['_auth_user_backend'])

    def test_invalid_username(self):
        """
        Test that login fails with an invalid username.
        """
        authenticated_user = authenticate(username='wronguser', password='testpassword')
        self.assertIsNone(authenticated_user)

    def test_invalid_password(self):
        """
        Test that login fails with an invalid password.
        """
        authenticated_user = authenticate(username='testuser', password='wrongpassword')
        self.assertIsNone(authenticated_user)

class SignUpViewTest(TestCase):  # :no-index: Abstract class for shared signup tests
    """
    Tests for the signup view.
    Abstract class for shared signup tests. Skipped during direct execution.
    """
    def setUp(self):
        if self.__class__ == SignUpViewTest:
            raise unittest.SkipTest("Abstract SignUpViewTest class - not intended for direct execution")
        self.client = Client()

    def test_signup_get(self):
        """
        Test that the signup page is accessible.
        """
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_signup_post_valid(self):
        """
        Test that a user can sign up with valid data.
        """
        form_data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'securepass', 'password2': 'securepass'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.profile_create_url)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='new_user')
        self.assertEqual(user.user_type, self.user_type)
        self.assertTrue(user.is_authenticated)

    def test_signup_post_invalid(self):
        """
        Test that signup fails with invalid data (e.g., passwords do not match).
        """
        form_data = {'username': 'bad_user', 'email': 'bad@example.com', 'password': 'short', 'password2': 'short'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context['form'], self.form_class)
        self.assertIn('password1', response.context['form'].errors)  # :no-index: Changed 'password' to 'password1'
        self.assertIn('password2', response.context['form'].errors)  # :no-index: Added assertion for 'password2'
        self.assertEqual(User.objects.count(), 0)

class LoginViewTest(TestCase):
    """
    Tests for the login view.
    """

    def setUp(self):
        """
        Set up test data for login tests.
        """
        self.client = Client()
        self.login_url = reverse('core:login')
        self.logout_url = reverse('core:logout')
        self.applicant = get_user_model().objects.create_user(
            username='test_applicant', password='testpass', user_type='applicant'
        )
        self.recruiter = get_user_model().objects.create_user(
            username='test_recruiter', password='testpass', user_type='recruiter'
        )
        # :no-index: Create the RecruiterProfile here:
        RecruiterProfile.objects.create(user=self.recruiter)  # :no-index: Assuming 'RecruiterProfile' model exists
        self.applicant_dashboard_url = reverse('applicant:applicant_dashboard')
        self.recruiter_dashboard_url = reverse('recruiter:recruiter_dashboard')
        self.home_url = reverse('core:home')

    def test_login_get(self):
        """
        Test that the login page is accessible.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

    def test_login_post_valid_applicant(self):
        """
        Test that an applicant can log in with valid credentials.
        """
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
        """
        Test that a recruiter can log in with valid credentials.
        """
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
        """
        Test that login fails with invalid credentials.
        """
        form_data = {'username': 'test_applicant', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIn('Please enter a correct username and password.', str(response.content))
        self.assertFalse(self.client.session.get('_auth_user_id'))


class LogoutViewTest(TestCase):
    """
    Tests for the logout view.
    """
    def setUp(self):
        """
        Set up test data for logout tests.
        """
        self.logout_url = reverse('core:logout')
        self.home_url = reverse('core:home')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword') # :no-index: Log in the client

    def test_logout_get(self):
        """
        Test that the logout page redirects to the home page after logout.
        """
        response = self.client.get(self.logout_url, follow=True) # :no-index: Follow the redirect
        self.assertEqual(response.status_code, 200) # :no-index: Expect a 200 on the redirected page (home)
        self.assertFalse(response.wsgi_request.user.is_authenticated) # :no-index: User should be logged out
        self.assertEqual(response.wsgi_request.path, self.home_url) # :no-index: Should be redirected to home

    def test_logout_post(self):
        """
        Test that a POST request to the logout page also logs the user out.
        """
        response = self.client.post(self.logout_url, follow=True) # :no-index: Follow the redirect
        self.assertEqual(response.status_code, 200) # :no-index: Expect a 200 on the redirected page (home)
        self.assertFalse(response.wsgi_request.user.is_authenticated) # :no-index: User should be logged out
        self.assertEqual(response.wsgi_request.path, self.home_url) # :no-index: Should be redirected to home

class ApplicantSignUpViewTest(TestCase):
    """
    Tests for the applicant signup view.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole class
        """
        Group.objects.create(name='Applicant')

    def setUp(self):
        """
        Set up the attributes to be used during testing
        """
        self.signup_url = reverse('core:applicant_signup')
        self.profile_create_url = reverse('applicant:applicant_profile_create')
        self.template_name = 'core/applicant_signup.html'
        self.form_class = ApplicantSignUpForm
        self.user_type = 'applicant'

    def test_signup_post_valid(self):
        """
        Test the view when a valid applicant sign up form is submitted
        """
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
    """
    Tests for the recruiter signup view.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up data for the whole class
        """
        Group.objects.create(name='Recruiter')

    def setUp(self):
        """
        Set up the attributes to be used during testing
        """
        self.signup_url = reverse('core:recruiter_signup')
        self.profile_create_url = reverse('recruiter:recruiter_profile_create')
        self.template_name = 'core/recruiter_signup.html'
        self.form_class = RecruiterSignUpForm
        self.user_type = 'recruiter'

    def test_signup_post_valid(self):
        """
        Test the view when a valid recruiter sign up form is submitted
        """
        # :no-index: Arrange
        form_data = {
            'username': 'testrecruiter',
            'email': 'recruiter@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        }
        # :no-index: Act
        response = self.client.post(self.signup_url, form_data, follow=True)
        # :no-index: Assert
        self.assertRedirects(response, self.profile_create_url)
        self.assertTrue(User.objects.filter(username='testrecruiter').exists())
        created_user = User.objects.get(username='testrecruiter')
        self.assertTrue(created_user.groups.filter(name='Recruiter').exists())

class CoreViewsTest(TestCase):
    """
    Tests for the core views
    """
    def setUp(self):
        """
        Set up the attributes to be used during testing
        """
        self.client = Client()

    def test_login_view_get(self):
        """
        Test if the login view returns a 200 status code
        """
        # :no-index: Act
        response = self.client.get(reverse('core:login'))
        # :no-index: Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIsInstance(response.context['form'], AuthenticationForm)

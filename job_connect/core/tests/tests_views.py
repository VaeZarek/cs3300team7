import unittest
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
        # 1. Simulate a successful login attempt
        form_data = {'username': 'test_applicant', 'password': 'testpass'}
        response = self.client.post(self.login_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.applicant_dashboard_url)

        # 2. **Crucially, check for authentication using client.login()**
        logged_in = self.client.login(username='test_applicant', password='testpass')
        self.assertTrue(logged_in)  # Assert that login was successful
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertTrue(self.client.session['_auth_user_backend'])

        # 3. **Verify user is authenticated in a subsequent request (most robust)**
        response = self.client.get(self.applicant_dashboard_url)
        self.assertEqual(response.status_code, 200)  # Or whatever status code is appropriate for your dashboard
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_valid_recruiter(self):
        # 1. Simulate a successful login attempt
        form_data = {'username': 'test_recruiter', 'password': 'testpass'}
        response = self.client.post(self.login_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.recruiter_dashboard_url)

        # 2. **Crucially, check for authentication using client.login()**
        logged_in = self.client.login(username='test_recruiter', password='testpass')
        self.assertTrue(logged_in)
        self.assertTrue(self.client.session['_auth_user_id'])

        # 3. **Verify user is authenticated in a subsequent request (most robust)**
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
        self.client = Client()
        self.login_url = reverse('core:login')
        self.logout_url = reverse('core:logout')
        self.applicant = get_user_model().objects.create_user(
            username='test_applicant', password='testpass', user_type='applicant'
        )
        self.recruiter = get_user_model().objects.create_user(
            username='test_recruiter', password='testpass', user_type='recruiter'
        )
        # Create a RecruiterProfile for the recruiter user
        RecruiterProfile.objects.create(user=self.recruiter)
        self.applicant_dashboard_url = reverse('applicant:applicant_dashboard')  # Assuming this URL name
        self.recruiter_dashboard_url = reverse('recruiter:recruiter_dashboard')  # Assuming this URL name
        self.home_url = reverse('core:home')

    def test_logout_get(self):
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(self.client.session.get('_auth_user_id'))

    def test_logout_post(self):
        response = self.client.post(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_url)
        self.assertFalse(self.client.session.get('_auth_user_id'))




class ApplicantSignUpViewTest(SignUpViewTest):
    def setUp(self):
        super().setUp()
        self.signup_url = reverse('core:applicant_signup')
        self.profile_create_url = reverse('applicant:applicant_profile_create')  # Assuming this URL name
        self.template_name = 'core/applicant_signup.html'
        self.form_class = ApplicantSignUpForm
        self.user_type = 'applicant'

    def test_signup_post_valid(self):
        form_data = {
            'username': 'testapplicant',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'password2': 'testpassword123'
        }
        print(f"\n--- Running test_signup_post_valid for applicant ---")
        print(f"Signup URL: {self.signup_url}")
        print(f"Profile Create URL: {self.profile_create_url}")
        print(f"Form Data: {form_data}")

        # Manually instantiate the form and check validity
        form = ApplicantSignUpForm(form_data)
        print(f"Is form valid before post? {form.is_valid()}")
        if not form.is_valid():
            print(f"Form errors: {form.errors}")

        response = self.client.post(self.signup_url, form_data, follow=True)

        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        print(f"Response content (first 500 chars): {response.content[:500].decode('utf-8') if response.content else 'No content'}")

        try:
            created_user = User.objects.get(username='testapplicant')
            print(f"User created successfully: {created_user}")
        except User.DoesNotExist:
            print("User NOT created!")

        print(f"Is user authenticated after post? {response.wsgi_request.user.is_authenticated}")

        self.assertRedirects(response, self.profile_create_url)
        self.assertTrue(User.objects.filter(username='testapplicant').exists())
        # You can add more assertions here, like checking if the user is in the 'Applicant' group


class RecruiterSignUpViewTest(SignUpViewTest):
    def setUp(self):
        super().setUp()
        self.signup_url = reverse('core:recruiter_signup')
        self.profile_create_url = reverse('recruiter:recruiter_profile_create')  # Assuming this URL name
        self.template_name = 'core/recruiter_signup.html'
        self.form_class = RecruiterSignUpForm
        self.user_type = 'recruiter'

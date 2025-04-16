from django.test import TestCase, Client
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login

from core.forms import ApplicantSignUpForm, RecruiterSignUpForm

User = get_user_model()


class AuthenticationViewTest(TestCase):  # Renamed for clarity

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.login_url = reverse('login')  # Replace 'login' with your actual login URL name

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


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.applicant = get_user_model().objects.create_user(
            username='test_applicant', password='testpass', user_type='applicant'
        )
        self.recruiter = get_user_model().objects.create_user(
            username='test_recruiter', password='testpass', user_type='recruiter'
        )
        self.applicant_dashboard_url = reverse('applicant_dashboard')  # Assuming this URL name
        self.recruiter_dashboard_url = reverse('recruiter_dashboard')  # Assuming this URL name
        self.home_url = reverse('home')  # Assuming this URL name

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
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')
        self.user = User.objects.create_user(username='logged_in_user', password='password', user_type='applicant')
        self.client.login(username='logged_in_user', password='password')
        self.assertTrue(self.client.session.get('_auth_user_id'))

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


class SignUpViewTest(TestCase):  # Abstract class for shared signup tests
    def setUp(self):
        self.client = Client()

    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.template_name)
        self.assertIsInstance(response.context['form'], self.form_class)

    def test_signup_post_valid(self):
        form_data = {'username': 'new_user', 'email': 'new_user@example.com', 'password': 'securepass', 'password2': 'securepass'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 302)
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
        self.assertIn('password', response.context['form'].errors)
        self.assertEqual(User.objects.count(), 0)


class ApplicantSignUpViewTest(SignUpViewTest):
    def setUp(self):
        super().setUp()
        self.signup_url = reverse('applicant_signup')
        self.profile_create_url = reverse('applicant_profile_create')  # Assuming this URL name
        self.template_name = 'core/applicant_signup.html'
        self.form_class = ApplicantSignUpForm
        self.user_type = 'applicant'


class RecruiterSignUpViewTest(SignUpViewTest):
    def setUp(self):
        super().setUp()
        self.signup_url = reverse('recruiter_signup')
        self.profile_create_url = reverse('recruiter_profile_create')  # Assuming this URL name
        self.template_name = 'core/recruiter_signup.html'
        self.form_class = RecruiterSignUpForm
        self.user_type = 'recruiter'

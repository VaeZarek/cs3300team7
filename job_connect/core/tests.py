from django.test import TestCase, Client
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm
from applicant.forms import ApplicantProfileForm  # Import forms used in redirects
from recruiter.forms import RecruiterProfileForm
from . import models  # Import your models

User = get_user_model()

class UserModelTest(TestCase):
    # ... (Your existing UserModel tests)
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            user_type='applicant'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.user_type, 'applicant')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword',
            email='admin@example.com'
        )
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertTrue(admin_user.check_password('adminpassword'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.user_type, '') # Default should be empty or handled elsewhere

    def test_is_applicant_method(self):
        applicant = User(username='applicant1', user_type='applicant')
        recruiter = User(username='recruiter1', user_type='recruiter')
        other = User(username='other1', user_type='other') # Assuming you might have other types

        self.assertTrue(applicant.is_applicant())
        self.assertFalse(recruiter.is_applicant())
        self.assertFalse(other.is_applicant())

    def test_is_recruiter_method(self):
        applicant = User(username='applicant1', user_type='applicant')
        recruiter = User(username='recruiter1', user_type='recruiter')
        other = User(username='other1', user_type='other') # Assuming you might have other types

        self.assertFalse(applicant.is_recruiter())
        self.assertTrue(recruiter.is_recruiter())
        self.assertFalse(other.is_recruiter())

    def test_user_type_choices(self):
        expected_choices = {('applicant', 'Applicant'), ('recruiter', 'Recruiter')}
        actual_choices = set(User._meta.get_field('user_type').choices)
        self.assertEqual(actual_choices, expected_choices)

    def test_groups_and_permissions_fields(self):
        user = User.objects.create_user(username='permsuser', password='password', user_type='applicant')
        self.assertTrue(hasattr(user, 'groups'))
        self.assertTrue(hasattr(user, 'user_permissions'))
        self.assertEqual(user._meta.get_field('groups').remote_field.name, 'group')
        self.assertEqual(user._meta.get_field('user_permissions').remote_field.name, 'permission')
        self.assertEqual(user._meta.get_field('groups').remote_field.related_name, 'core_user_set')
        self.assertEqual(user._meta.get_field('user_permissions').remote_field.related_name, 'core_user_permissions_set')


class BaseModelTest(TestCase):
    # ... (Your existing BaseModel tests)
    def test_base_model_creation(self):
        class TestModel(models.Model):  # Use models from import
            name = models.CharField(max_length=100)
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)

            class Meta:
                abstract = True

        class ConcreteModel(TestModel):
            pass

        obj = ConcreteModel.objects.create(name='Test Object')
        self.assertIsNotNone(obj.created_at)
        self.assertIsNotNone(obj.updated_at)
        self.assertLessEqual(obj.created_at, obj.updated_at)

    def test_base_model_updated_at_changes(self):
        import time
        class TestModel(models.Model):  # Use models from import
            name = models.CharField(max_length=100)
            created_at = models.DateTimeField(auto_now_add=True)
            updated_at = models.DateTimeField(auto_now=True)

            class Meta:
                abstract = True

        class ConcreteModel(TestModel):
            pass

        obj = ConcreteModel.objects.create(name='Initial')
        initial_updated_at = obj.updated_at
        time.sleep(1) # Ensure some time passes
        obj.name = 'Updated'
        obj.save()
        self.assertNotEqual(initial_updated_at, obj.updated_at)
        self.assertLess(initial_updated_at, obj.updated_at)


class ApplicantSignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('applicant_signup')
        self.profile_create_url = reverse('applicant_profile_create')  # Assuming this URL name

    def test_applicant_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/applicant_signup.html')
        self.assertIsInstance(response.context['form'], ApplicantSignUpForm)

    def test_applicant_signup_post_valid(self):
        form_data = {'username': 'new_applicant', 'email': 'new_applicant@example.com', 'password': 'securepass', 'password2': 'securepass'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_create_url)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='new_applicant')
        self.assertEqual(user.user_type, 'applicant')
        self.assertTrue(user.is_authenticated)

    def test_applicant_signup_post_invalid(self):
        form_data = {'username': 'bad_applicant', 'email': 'bad@example.com', 'password': 'short', 'password2': 'short'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/applicant_signup.html')
        self.assertIsInstance(response.context['form'], ApplicantSignUpForm)
        self.assertIn('password', response.context['form'].errors)
        self.assertEqual(User.objects.count(), 0)

class RecruiterSignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('recruiter_signup')
        self.profile_create_url = reverse('recruiter_profile_create')  # Assuming this URL name

    def test_recruiter_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/recruiter_signup.html')
        self.assertIsInstance(response.context['form'], RecruiterSignUpForm)

    def test_recruiter_signup_post_valid(self):
        form_data = {'username': 'new_recruiter', 'email': 'new_recruiter@example.com', 'password': 'strongpass', 'password2': 'strongpass'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_create_url)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='new_recruiter')
        self.assertEqual(user.user_type, 'recruiter')
        self.assertTrue(user.is_authenticated)

    def test_recruiter_signup_post_invalid(self):
        form_data = {'username': 'bad_recruiter', 'email': 'bad_r@example.com', 'password': 'weak', 'password2': 'weak'}
        response = self.client.post(self.signup_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/recruiter_signup.html')
        self.assertIsInstance(response.context['form'], RecruiterSignUpForm)
        self.assertIn('password', response.context['form'].errors)
        self.assertEqual(User.objects.count(), 0)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.applicant = User.objects.create_user(username='test_applicant', password='testpass', user_type='applicant')
        self.recruiter = User.objects.create_user(username='test_recruiter', password='testpass', user_type='recruiter')
        self.applicant_dashboard_url = reverse('applicant_dashboard') # Assuming this URL name
        self.recruiter_dashboard_url = reverse('recruiter_dashboard') # Assuming this URL name
        self.home_url = reverse('home') # Assuming this URL name

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
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertEqual(self.client.session['_auth_user_backend'], 'django.contrib.auth.backends.ModelBackend')
        self.assertEqual(str(self.client.session['_auth_user_hash']), self.applicant.password) # Basic check

    def test_login_post_valid_recruiter(self):
        form_data = {'username': 'test_recruiter', 'password': 'testpass'}
        response = self.client.post(self.login_url, form_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.recruiter_dashboard_url)
        self.assertTrue(self.client.session['_auth_user_id'])
        self.assertEqual(str(self.client.session['_auth_user_hash']), self.recruiter.password) # Basic check

    def test_login_post_invalid_credentials(self):
        form_data = {'username': 'test_applicant', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/login.html')
        self.assertIn('Invalid username and/or password.', str(response.content))
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
from django.test import TestCase
from django.contrib.auth.models import User
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm
from applicant.forms import ApplicantProfileForm
from recruiter.forms import RecruiterProfileForm
from recruiter.models import RecruiterProfile
from applicant.models import ApplicantProfile


class CoreFormsTest(TestCase):
    def test_applicant_signup_form(self):
        form_data = {
            'username': 'testapplicant',
            'email': 'test@example.com',
            'password2': 'securepassword123',
            'password': 'securepassword123',
        }
        form = ApplicantSignUpForm(data=form_data)
        print(f"\n--- test_applicant_signup_form (valid) ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_applicant_signup_form_invalid(self):
        form_data = {
            'username': 'testapplicant',
            'email': 'invalid-email',
            'password2': 'short',
            'password': 'short',  # Use 'password'
        }
        form = ApplicantSignUpForm(data=form_data)
        print(f"\n--- test_applicant_signup_form_invalid ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertIn('password2', form.errors)  # Check for error in 'password2'
        self.assertIn('This password is too short', str(form.errors['password2']))

    def test_recruiter_signup_form(self):
        form_data = {
            'username': 'testrecruiter',
            'email': 'recruiter@example.com',
            'password2': 'strongpassword456',
            'password': 'strongpassword456',
        }
        form = RecruiterSignUpForm(data=form_data)
        print(f"\n--- test_recruiter_signup_form (valid) ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

class ApplicantProfileFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user)

    def test_applicant_profile_form(self):
        # Provide valid data based on your form fields
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile) # Pass instance if needed
        print(f"\n--- test_applicant_profile_form (valid) ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_applicant_profile_form_invalid(self):
        form_data = {} # Providing no data - 'headline' and 'summary' are likely required
        form = ApplicantProfileForm(data=form_data)
        print(f"\n--- test_applicant_profile_form_invalid ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())

class RecruiterProfileFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testrecruiter', password='testpassword')
        self.recruiter_profile = RecruiterProfile.objects.create(user=self.user)

    def test_recruiter_profile_form(self):
        # Provide valid data based on your form fields
        form_data = {'company_name': 'Test Company', 'company_website': 'https://test.com', 'description': 'Test Description'}
        form = RecruiterProfileForm(data=form_data, instance=self.recruiter_profile) # Pass instance if needed
        print(f"\n--- test_recruiter_profile_form (valid) ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_recruiter_profile_form_invalid(self):
        form_data = {} # Providing no data - all fields are likely required
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_invalid ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())
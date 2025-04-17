from django.test import TestCase
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm
from applicant.forms import ApplicantProfileForm
from recruiter.forms import RecruiterProfileForm


class CoreFormsTest(TestCase):
    def test_applicant_signup_form(self):
        form_data = {
            'username': 'testapplicant',
            'email': 'test@example.com',
            'password': 'securepassword',
            'password_confirm': 'securepassword',
        }
        form = ApplicantSignUpForm(data=form_data)
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())  # Your assertion

    def test_applicant_signup_form_invalid(self):
        form_data = {
            'username': 'testapplicant',
            'email': 'invalid-email',
            'password': 'short',
            'password_confirm': 'mismatch',
        }
        form = ApplicantSignUpForm(data=form_data)
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertIn('password', form.errors)

    def test_recruiter_signup_form(self):
        form_data = {'username': 'test', 'email': 'test@test.com', 'password': 'testpass', 'password2': 'testpass'}
        form = RecruiterSignUpForm(form_data)
        self.assertTrue(form.is_valid())

    def test_recruiter_signup_form_invalid(self):
        form_data = {'username': 'test', 'email': 'test@test.com', 'password': 'short', 'password2': 'short'}
        form = RecruiterSignUpForm(form_data)
        self.assertFalse(form.is_valid())
        #print(form.errors.keys())  # Print the error keys
        self.assertIn('password2', form.errors)  # Or 'password1' if that's the key


class ApplicantProfileFormsTest(TestCase):
    def test_applicant_profile_form(self):
        form_data = {'field1': 'test_field1', 'field2': 'test_field2'}  # Replace with actual form data
        form = ApplicantProfileForm(form_data)
        self.assertTrue(form.is_valid())

    def test_applicant_profile_form_invalid(self):
        form_data = {}  # Replace with invalid form data
        form = ApplicantProfileForm(form_data)
        self.assertFalse(form.is_valid())


class RecruiterProfileFormsTest(TestCase):
    def test_recruiter_profile_form(self):
        form_data = {'field1': 'test_field1', 'field2': 'test_field2'}  # Replace with actual form data
        form = RecruiterProfileForm(form_data)
        self.assertTrue(form.is_valid())

    def test_recruiter_profile_form_invalid(self):
        form_data = {}  # Replace with invalid form data
        form = RecruiterProfileForm(form_data)
        self.assertFalse(form.is_valid())
from django.test import TestCase
from core.models import User
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
            'password1': 'securepassword123', # Use 'password1'
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
            'password1': 'short', # Use 'password1'
        }
        form = ApplicantSignUpForm(data=form_data)
        print(f"\n--- test_applicant_signup_form_invalid ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertIn('password2', form.errors) # Keep assertion on password2
        self.assertIn('This password is too short', str(form.errors['password2']))

    def test_recruiter_signup_form(self):
        form_data = {
            'username': 'testrecruiter',
            'email': 'recruiter@example.com',
            'password2': 'strongpassword456',
            'password1': 'strongpassword456', # Use 'password1'
        }
        form = RecruiterSignUpForm(data=form_data)
        print(f"\n--- test_recruiter_signup_form (valid) ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())




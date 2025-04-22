from django.test import TestCase
from django.contrib.auth import get_user_model
from core.forms import ApplicantSignUpForm, RecruiterSignUpForm

User = get_user_model()

class ApplicantSignupFormTests(TestCase):
    """
    Tests for the applicant signup form.
    """

    def test_applicant_signup_form(self):
        """
        Test that the applicant signup form is valid with valid data.
        """
        form_data = {
            'username': 'testapplicant',
            'email': 'test@example.com',
            'password2': 'securepassword123',
            'password1': 'securepassword123', # :no-index: Use 'password1'
        }
        form = ApplicantSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_applicant_signup_form_invalid(self):
        """
        Test that the applicant signup form is valid with invalid data.
        """
        form_data = {
            'username': 'testapplicant',
            'email': 'invalid-email',
            'password2': 'short',
            'password1': 'short', # :no-index: Use 'password1'
        }
        form = ApplicantSignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors) # :no-index: Keep assertion on password2
        self.assertIn('This password is too short', str(form.errors['password2']))

    def test_recruiter_signup_form(self):
        """
        Tests for the recruiter signup form.
        """
        form_data = {
            'username': 'testrecruiter',
            'email': 'recruiter@example.com',
            'password2': 'strongpassword456',
            'password1': 'strongpassword456', # :no-index: Use 'password1'
        }
        form = RecruiterSignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
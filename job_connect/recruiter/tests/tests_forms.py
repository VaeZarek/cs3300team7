from django.test import TestCase
from django.contrib.auth import get_user_model
from recruiter.forms import RecruiterProfileForm
from recruiter.models import RecruiterProfile

User = get_user_model()

class RecruiterProfileFormsTest(TestCase):
    """
    Tests for the RecruiterProfileForm.
    """

    def test_recruiter_profile_form_valid_data(self):
        """
        Test that the recruiter profile form is valid with valid data.
        """
        user = User.objects.create_user(username='testrecruiter1')
        form_data = {
            'company_name': 'Test Company',
            'company_website': 'https://test.com',
            'description': 'A brief description.',
            'location': 'Test Location'
        }
        form = RecruiterProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        self.assertEqual(RecruiterProfile.objects.count(), 1)
        retrieved_profile = RecruiterProfile.objects.get(user=user)
        self.assertEqual(retrieved_profile.company_name, 'Test Company')

    def test_recruiter_profile_form_description_max_length(self):
        """
        Test that the recruiter profile form enforces the maximum length for the description field.
        """
        long_description = 'a' * 501
        form_data = {
            'company_name': 'Test Company',
            'description': long_description
        }
        form = RecruiterProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)

    def test_recruiter_profile_form_invalid(self):
        """
        Test that the recruiter profile form is invalid with empty data.
        """
        form = RecruiterProfileForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_recruiter_profile_form_invalid_website_format(self):
        """
        Test that the recruiter profile form is invalid with an invalid website format.
        """
        form_data = {'company_name': 'Test', 'company_website': 'invalid-url'}
        form = RecruiterProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('company_website', form.errors)

    def test_recruiter_profile_form_missing_required_fields(self):
        """
        Test that the recruiter profile form is invalid when missing required fields.
        """
        form = RecruiterProfileForm(data={'description': 'test'})
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_recruiter_profile_form_optional_fields_empty(self):
        """
        Test that the recruiter profile form is valid when optional fields are empty.
        """
        user = User.objects.create_user(username='testrecruiter2')
        form_data = {'company_name': 'Test Company'}
        form = RecruiterProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        self.assertEqual(RecruiterProfile.objects.count(), 1)
        retrieved_profile = RecruiterProfile.objects.get(user=user)
        self.assertEqual(retrieved_profile.company_name, 'Test Company')
        self.assertEqual(retrieved_profile.company_website, '')
        self.assertEqual(retrieved_profile.description, '')
        self.assertEqual(retrieved_profile.location, '')

    def test_recruiter_profile_form_save(self):
        """
        Test that the recruiter profile form saves correctly.
        """
        user = User.objects.create_user(username='testrecruiter3')  # Create a unique user
        form_data = {
            'company_name': 'Another Test Company',
            'company_website': 'https://anothertest.com',
            'description': 'Another brief description.',
            'location': 'Another Test Location'
        }
        form = RecruiterProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
        profile = form.save(commit=False)
        profile.user = user
        profile.save()
        self.assertEqual(RecruiterProfile.objects.count(), 1)
        retrieved_profile = RecruiterProfile.objects.get(user=user)
        self.assertEqual(retrieved_profile.company_name, 'Another Test Company')
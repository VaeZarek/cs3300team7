from django.test import TestCase
from core.models import User
from recruiter.forms import RecruiterProfileForm
from recruiter.models import RecruiterProfile


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
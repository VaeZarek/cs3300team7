from django.test import TestCase
from core.models import User
from applicant.forms import ApplicantProfileForm
from applicant.models import ApplicantProfile


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
from django.test import TestCase
from core.models import User
from applicant.forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
from applicant.models import ApplicantProfile


class ApplicantProfileFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user)

    def test_applicant_profile_form_valid(self):
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_invalid_missing_headline(self):
        form_data = {'summary': 'Test Summary', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('headline', form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_applicant_profile_form_invalid_missing_summary(self):
        form_data = {'headline': 'Test Headline', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('summary', form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_applicant_profile_form_valid_empty_skills_resume(self):
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [], 'resume': ''}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_with_skills(self):
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [1, 2], 'resume': None}
        # Assuming you have some Skill objects with IDs 1 and 2 in your test database
        # If not, you might need to create them in setUpTestData or setUp
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    # Add tests for max_length if defined in your ApplicantProfile model
    # Example (assuming headline has max_length=255 in the model):
    def test_applicant_profile_form_invalid_headline_too_long(self):
        long_headline = 'a' * 300
        form_data = {'headline': long_headline, 'summary': 'Test Summary', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('headline', form.errors)

    # Similarly, add a test for summary if it has a max_length

    def test_experience_formset_valid(self):
        form_data = {
            'experiences-TOTAL_FORMS': '1',
            'experiences-INITIAL_FORMS': '0',
            'experiences-MIN_NUM_FORMS': '0',
            'experiences-MAX_NUM_FORMS': '1000',
            'experiences-0-title': 'Software Engineer',
            'experiences-0-company': 'Tech Corp',
            'experiences-0-start_date': '2023-01-01',
            'experiences-0-end_date': '2024-01-01',
            'experiences-0-description': 'Developed key features.',
            'experiences-0-DELETE': False,
        }
        formset = ExperienceFormSet(data=form_data, instance=self.applicant_profile)
        print(f"\n--- test_experience_formset_valid ---")
        print(f"Is formset valid? {formset.is_valid()}")
        print(f"Formset errors: {formset.errors}")
        for form in formset.forms:
            print(f"Form errors: {form.errors}")
        self.assertTrue(formset.is_valid())

    # Add more tests for ExperienceFormSet (invalid data, empty, etc.)

    def test_education_formset_valid(self):
        form_data = {
            'educations-TOTAL_FORMS': '1',
            'educations-INITIAL_FORMS': '0',
            'educations-MIN_NUM_FORMS': '0',
            'educations-MAX_NUM_FORMS': '1000',
            'educations-0-degree': 'Master of Science',
            'educations-0-institution': 'University X',
            'educations-0-graduation_date': '2022-05-01',
            'educations-0-major': 'Computer Science',
            'educations-0-DELETE': False,
        }
        formset = EducationFormSet(data=form_data, instance=self.applicant_profile)
        print(f"\n--- test_education_formset_valid ---")
        print(f"Is formset valid? {formset.is_valid()}")
        print(f"Formset errors: {formset.errors}")
        for form in formset.forms:
            print(f"Form errors: {form.errors}")
        self.assertTrue(formset.is_valid())

    # Add more tests for EducationFormSet
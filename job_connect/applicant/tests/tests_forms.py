from django.test import TestCase
from core.models import User
from applicant.forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
from applicant.models import ApplicantProfile, Skill
from datetime import date


class ApplicantProfileFormsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testapplicant', password='testpassword')
        cls.applicant_profile = ApplicantProfile.objects.create(user=cls.user)
        cls.python_skill = Skill.objects.create(name='Python')
        cls.django_skill = Skill.objects.create(name='Django')

    def test_applicant_profile_form_valid(self):
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_invalid_missing_headline(self):
        form_data = {'summary': 'Test Summary', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('headline', form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_applicant_profile_form_invalid_missing_summary(self):
        form_data = {'headline': 'Test Headline', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
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
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_invalid_headline_too_long(self):
        long_headline = 'a' * 300
        form_data = {'headline': long_headline, 'summary': 'Test Summary', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('headline', form.errors)

    def test_experience_formset_valid_single_form(self):
        from datetime import date
        form_data = {
            'experiences-TOTAL_FORMS': '1',
            'experiences-INITIAL_FORMS': '0',
            'experiences-MIN_NUM_FORMS': '0',
            'experiences-MAX_NUM_FORMS': '1000',
            'experiences-0-title': 'Software Engineer',
            'experiences-0-company': 'Tech Corp',
            'experiences-0-start_date': date(2023, 1, 1),
            'experiences-0-end_date': date(2024, 1, 1),
            'experiences-0-description': 'Developed key features.',
            'experiences-0-DELETE': False,
        }
        formset = ExperienceFormSet(data=form_data, instance=self.applicant_profile)
        print(f"\n--- test_experience_formset_valid_single_form ---")
        print(f"Is formset valid? {formset.is_valid()}")
        print(f"Formset errors: {formset.errors}")
        print(f"Non-form errors: {formset.non_form_errors()}")
        for form in formset.forms:
            print(f"Form errors: {form.errors}")
            print(f"Form cleaned_data: {form.cleaned_data}")

        self.assertTrue(formset.is_valid())
        print(f"Formset errors list: {formset.errors}")
        self.assertEqual(formset.errors, [])  # Check if the list is empty
        self.assertTrue(formset.forms[0].is_valid())
        self.assertEqual(len(formset.forms[0].errors), 0)

    def test_experience_formset_invalid_missing_required_field(self):
        form_data = {
            'experiences-TOTAL_FORMS': '1',
            'experiences-INITIAL_FORMS': '0',
            'experiences-MIN_NUM_FORMS': '0',
            'experiences-MAX_NUM_FORMS': '1000',
            'experiences-0-title': '',  # Missing title
            'experiences-0-company': 'Tech Corp',
            'experiences-0-start_date': '2023-01-01',
            'experiences-0-end_date': '2024-01-01',
            'experiences-0-description': 'Developed key features.',
            'experiences-0-DELETE': False,
        }
        formset = ExperienceFormSet(data=form_data, instance=self.applicant_profile)
        self.assertFalse(formset.is_valid())
        self.assertEqual(len(formset.errors), 1)  # Formset itself might have an error related to the form
        self.assertFalse(formset.forms[0].is_valid())
        self.assertIn('title', formset.forms[0].errors)

    # Add more tests for ExperienceFormSet (e.g., invalid date format)

    def test_education_formset_valid_single_form(self):
        # We'll add this and invalid tests for EducationFormSet next
        pass

    def test_education_formset_invalid_missing_required_field(self):
        pass

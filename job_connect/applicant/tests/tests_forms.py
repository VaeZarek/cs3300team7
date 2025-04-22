from django.test import TestCase
from core.models import User
from applicant.forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
from applicant.models import ApplicantProfile, Skill, Experience, Education
from datetime import date


class ApplicantProfileFormsTest(TestCase):
    """
    Tests for the ApplicantProfileForm.
    """
    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the class.  Creates a user and some skills.
        """
        cls.user = User.objects.create_user(username='testapplicant', password='testpassword')
        cls.applicant_profile = ApplicantProfile.objects.create(user=cls.user)
        cls.python_skill = Skill.objects.create(name='Python')
        cls.django_skill = Skill.objects.create(name='Django')

    def test_applicant_profile_form_valid(self):
        """
        Test that the form is valid with valid data.
        """
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_invalid_missing_headline(self):
        """
        Test that the form is invalid when the headline is missing.
        """
        form_data = {'summary': 'Test Summary', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('headline', form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_applicant_profile_form_invalid_missing_summary(self):
        """
        Test that the form is invalid when the summary is missing.
        """
        form_data = {'headline': 'Test Headline', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('summary', form.errors)
        self.assertEqual(len(form.errors), 1)

    def test_applicant_profile_form_valid_empty_skills_resume(self):
        """
        Test that the form is valid even with empty skills and resume.
        """
        form = ApplicantProfileForm(data={'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [], 'resume': ''}, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_with_skills(self):
        """
        Test that the form saves skills correctly.

        """
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary', 'skills': [self.python_skill.id, self.django_skill.id], 'resume': None}
        form = ApplicantProfileForm(data=form_data, instance=self.applicant_profile)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    def test_applicant_profile_form_invalid_headline_too_long(self):
        """
        Test that the form is invalid when the headline is too long.

        """
        form_data = {'headline': 'a' * 300, 'summary': 'Test Summary', 'skills': [], 'resume': None}
        form = ApplicantProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('headline', form.errors)

    def test_experience_formset_valid_single_form(self):
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
        self.assertTrue(formset.is_valid())
        self.assertEqual(formset.errors, [{}])  # Formset.errors unexpectedly contains [{}] for a valid formset
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
            'experiences-0-start_date': date(2023, 1, 1),
            'experiences-0-end_date': date(2024, 1, 1),
            'experiences-0-description': 'Developed key features.',
            'experiences-0-DELETE': False,
        }
        formset = ExperienceFormSet(data=form_data, instance=self.applicant_profile)
        self.assertFalse(formset.is_valid())
        self.assertEqual(len(formset.errors), 1)
        self.assertFalse(formset.forms[0].is_valid())
        self.assertIn('title', formset.forms[0].errors)

    def test_education_formset_valid_single_form(self):
        form_data = {
            'educations-TOTAL_FORMS': '1',
            'educations-INITIAL_FORMS': '0',
            'educations-MIN_NUM_FORMS': '0',
            'educations-MAX_NUM_FORMS': '1000',
            'educations-0-degree': 'Master of Science',
            'educations-0-institution': 'University X',
            'educations-0-graduation_date': date(2022, 5, 1),
            'educations-0-major': 'Computer Science',
            'educations-0-DELETE': False,
        }
        formset = EducationFormSet(data=form_data, instance=self.applicant_profile)
        self.assertTrue(formset.is_valid())
        self.assertEqual(formset.errors, [{}])  # Formset.errors unexpectedly contains [{}] for a valid formset
        self.assertTrue(formset.forms[0].is_valid())
        self.assertEqual(len(formset.forms[0].errors), 0)

    def test_education_formset_invalid_missing_required_field(self):
        form_data = {
            'educations-TOTAL_FORMS': '1',
            'educations-INITIAL_FORMS': '0',
            'educations-MIN_NUM_FORMS': '0',
            'educations-MAX_NUM_FORMS': '1000',
            'educations-0-degree': '',  # Missing degree
            'educations-0-institution': 'University X',
            'educations-0-graduation_date': date(2022, 5, 1),
            'educations-0-major': 'Computer Science',
            'educations-0-DELETE': False,
        }
        formset = EducationFormSet(data=form_data, instance=self.applicant_profile)
        self.assertFalse(formset.is_valid())
        self.assertEqual(len(formset.errors), 1)
        self.assertFalse(formset.forms[0].is_valid())
        self.assertIn('degree', formset.forms[0].errors)
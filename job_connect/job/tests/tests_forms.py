from django import forms
from django.test import TestCase
from job.forms import JobForm
from applicant.models import Skill
from recruiter.models import RecruiterProfile
from django.contrib.auth import get_user_model  # :no-index: Import get_user_model
from datetime import date
from job.models import Job

User = get_user_model()  # :no-index: Assign the custom user model to User

class JobFormTest(TestCase):
    """
    Tests for the JobForm.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the JobFormTest.
        """
        # :no-index: Create a recruiter profile and some skills for testing
        user = User.objects.create_user(username='test_recruiter', password='test_password')
        cls.recruiter_profile = RecruiterProfile.objects.create(user=user, company_name='Test Corp')
        Skill.objects.create(name='Python')
        Skill.objects.create(name='Django')
        cls.python_skill = Skill.objects.get(name='Python')
        cls.django_skill = Skill.objects.get(name='Django')

    def test_valid_job_form(self):
        """
        Test that a valid JobForm is valid.
        """
        # :no-index: Prepare valid form data
        form_data = {
            'title': 'Software Engineer',
            'description': 'Write code and stuff.',
            'requirements': 'Strong coding skills.',
            'location': 'Tech Hub',
            'salary_range': '$80k - $120k',
            'employment_type': 'Full-time',
            'application_deadline': date(2025, 5, 15),
            'is_active': True,
            'skills_required': [self.python_skill.id, self.django_skill.id],
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())
        job = form.save(commit=False)
        job.recruiter = self.recruiter_profile
        job.save()
        form.save_m2m()
        # :no-index: Retrieve the job from the database to ensure M2M is saved
        retrieved_job = Job.objects.get(pk=job.pk)
        self.assertEqual(retrieved_job.title, 'Software Engineer')
        self.assertEqual(retrieved_job.description, 'Write code and stuff.')
        self.assertEqual(retrieved_job.location, 'Tech Hub')
        self.assertEqual(retrieved_job.requirements, 'Strong coding skills.')
        self.assertEqual(retrieved_job.salary_range, '$80k - $120k')
        self.assertEqual(retrieved_job.employment_type, 'Full-time')
        self.assertEqual(retrieved_job.application_deadline, date(2025, 5, 15))
        self.assertTrue(retrieved_job.is_active)
        self.assertEqual(list(retrieved_job.skills_required.all()), [self.python_skill, self.django_skill])

    def test_invalid_job_form_missing_required_fields(self):
        """
        Test that a JobForm is invalid when missing required fields.
        """
        # :no-index: Prepare form data with missing required fields
        required_fields = ['title', 'description', 'location']
        for field in required_fields:
            form_data = {
                'title': 'Software Engineer',
                'description': 'Write code and stuff.',
                'requirements': 'Strong coding skills.',
                'location': 'Tech Hub',
                'salary_range': '$80k - $120k',
                'employment_type': 'Full-time',
                'application_deadline': date(2025, 5, 15),
                'is_active': True,
                'skills_required': [self.python_skill.id],
            }
            del form_data[field]
            form = JobForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn(field, form.errors)
            self.assertEqual(len(form.errors[field]), 1)
            self.assertEqual(form.errors[field][0], 'This field is required.')

    def test_valid_job_form_optional_fields_missing(self):
        """
        Test that a JobForm is valid when optional fields are missing.
        """
        # :no-index: Prepare valid form data with optional fields missing
        form_data = {
            'title': 'Software Engineer',
            'description': 'Write code and stuff.',
            'location': 'Tech Hub',
            'is_active': True,  # :no-index: Explicitly set is_active to True
            # :no-index: 'requirements', 'salary_range', 'employment_type', 'application_deadline', 'skills_required' are missing
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())
        job = form.save(commit=False)
        job.recruiter = self.recruiter_profile
        job.save()
        self.assertEqual(job.title, 'Software Engineer')
        self.assertEqual(job.description, 'Write code and stuff.')
        self.assertEqual(job.location, 'Tech Hub')
        self.assertEqual(job.requirements, '')
        self.assertEqual(job.salary_range, '')
        self.assertEqual(job.employment_type, '')
        self.assertIsNone(job.application_deadline)
        self.assertTrue(job.is_active)
        self.assertEqual(list(job.skills_required.all()), [])

    def test_job_form_invalid_application_deadline_type(self):
        """
        Test that a JobForm is invalid when the application deadline is of an invalid type.
        """
        # :no-index: Prepare form data with an invalid application deadline type
        form_data = {
            'title': 'Software Engineer',
            'description': 'Write code and stuff.',
            'requirements': 'Strong coding skills.',
            'location': 'Tech Hub',
            'salary_range': '$80k - $120k',
            'employment_type': 'Full-time',
            'application_deadline': 'not a date',
            'is_active': True,
            'skills_required': [self.python_skill.id],
        }
        form = JobForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('application_deadline', form.errors)
        self.assertEqual(len(form.errors['application_deadline']), 1)
        self.assertIn('Enter a valid date.', form.errors['application_deadline'][0])

    def test_job_form_empty_skills_required(self):
        """
        Test that a JobForm is valid when no skills are required.
        """
        form_data = {
            'title': 'Software Engineer',
            'description': 'Write code and stuff.',
            'requirements': 'Strong coding skills.',
            'location': 'Tech Hub',
            'salary_range': '$80k - $120k',
            'employment_type': 'Full-time',
            'application_deadline': date(2025, 5, 15),
            'is_active': True,
            'skills_required': [],
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())
        job = form.save(commit=False)
        job.recruiter = self.recruiter_profile
        job.save()
        self.assertEqual(list(job.skills_required.all()), [])
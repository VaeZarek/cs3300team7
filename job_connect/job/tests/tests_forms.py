from django import forms
from django.test import TestCase
from job.forms import JobForm
from applicant.models import Skill  # Correct import
from datetime import date

class JobFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Skill.objects.create(name='Python')
        Skill.objects.create(name='Django')
        cls.python_skill = Skill.objects.get(name='Python')
        cls.django_skill = Skill.objects.get(name='Django')

    def test_valid_job_form(self):
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
        self.assertEqual(job.title, 'Software Engineer')
        self.assertEqual(job.description, 'Write code and stuff.')
        self.assertEqual(job.location, 'Tech Hub')
        self.assertEqual(job.application_deadline, date(2025, 5, 15))
        self.assertTrue(job.is_active)
        self.assertEqual(list(job.skills_required.all()), [self.python_skill, self.django_skill])

    def test_invalid_job_form_missing_required_fields(self):
        required_fields = ['title', 'description', 'location', 'employment_type']
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
        form_data = {
            'title': 'Software Engineer',
            'description': 'Write code and stuff.',
            'location': 'Tech Hub',
            'employment_type': 'Full-time',
            # 'requirements', 'salary_range', 'application_deadline', 'is_active', 'skills_required' are missing
        }
        form = JobForm(data=form_data)
        self.assertTrue(form.is_valid())
        job = form.save(commit=False)
        self.assertEqual(job.title, 'Software Engineer')
        self.assertEqual(job.description, 'Write code and stuff.')
        self.assertEqual(job.location, 'Tech Hub')
        self.assertIsNone(job.requirements)
        self.assertIsNone(job.salary_range)
        self.assertIsNone(job.application_deadline)
        self.assertFalse(job.is_active) # Default value in model? Adjust if different.
        self.assertEqual(list(job.skills_required.all()), [])

    def test_job_form_invalid_application_deadline_type(self):
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
        self.assertEqual(list(job.skills_required.all()), [])
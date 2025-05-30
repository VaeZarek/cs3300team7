from django.test import TestCase
from job.models import Job
from recruiter.models import RecruiterProfile
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class JobModelTest(TestCase):
    """
    Tests for the Job model.
    """

    def setUp(self):
        """
        Set up the test environment for JobModelTest.
        """
        self.user = User.objects.create_user(username='testrecruiter', password='testpassword')
        self.recruiter_profile = RecruiterProfile.objects.create(user=self.user, company_name='Test Corp')

    def test_create_job(self):
        """
        Test that a Job can be created successfully.
        """
        job = Job.objects.create(
            recruiter=self.recruiter_profile,
            title='Software Engineer',
            description='Looking for a talented engineer.',
            location='Remote'
        )
        self.assertTrue(isinstance(job, Job))
        self.assertEqual(job.title, 'Software Engineer')
        self.assertEqual(job.recruiter, self.recruiter_profile)
        self.assertEqual(job.is_active, True) # :no-index: Check default value

    def test_job_fields(self):
        """
        Test that all fields of a Job are saved correctly.
        """
        job = Job.objects.create(
            recruiter=self.recruiter_profile,
            title='Product Manager',
            description='Manage our product roadmap.',
            requirements='3+ years experience.',
            location='New York',
            salary_range='$100k - $150k',
            employment_type='Full-time',
            application_deadline=date(2025, 5, 1),  # :no-index: Use date object here
            is_active=False
        )
        self.assertEqual(job.title, 'Product Manager')
        self.assertEqual(job.requirements, '3+ years experience.')
        self.assertEqual(job.location, 'New York')
        self.assertEqual(job.salary_range, '$100k - $150k')
        self.assertEqual(job.employment_type, 'Full-time')
        self.assertEqual(job.application_deadline.strftime('%Y-%m-%d'), '2025-05-01')
        self.assertFalse(job.is_active)
        self.assertIsNotNone(job.posted_date) # :no-index: Auto-now-add

    def test_job_recruiter_relationship(self):
        """
        Test the relationship between Job and RecruiterProfile.
        """
        job = Job.objects.create(
            recruiter=self.recruiter_profile,
            title='Data Scientist',
            description='Analyze our data.',
            location='San Francisco'
        )
        self.assertEqual(job.recruiter.company_name, 'Test Corp')
        self.assertIn(job, self.recruiter_profile.jobs.all())

    def test_job_str_method(self):
        """
        Test the __str__ method of the Job model.
        """
        job = Job.objects.create(
            recruiter=self.recruiter_profile,
            title='UX Designer',
            description='Design user interfaces.',
            location='Austin'
        )
        self.assertEqual(str(job), 'UX Designer')

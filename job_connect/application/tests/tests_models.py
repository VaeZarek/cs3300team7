from django.test import TestCase
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile, Skill
from recruiter.models import RecruiterProfile
from job.models import Job
from application.models import Application
from datetime import date
from django.core.files.base import ContentFile

User = get_user_model()

class ApplicationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for the applicant profile
        user_applicant = User.objects.create_user(username='applicant1', password='testpassword')
        cls.applicant_profile = ApplicantProfile.objects.create(
            user=user_applicant,
            headline='Experienced Developer',
            summary='A summary of my skills and experience.'
        )
        cls.skill = Skill.objects.create(name='Python')
        cls.applicant_profile.skills.add(cls.skill)

        # Create a user and recruiter profile for the job
        user_recruiter = User.objects.create_user(username='recruiter1', password='testpassword')
        cls.recruiter_profile = RecruiterProfile.objects.create(
            user=user_recruiter,
            company_name='Test Corp',
            location='Remote'
        )
        cls.job = Job.objects.create(
            recruiter=cls.recruiter_profile,
            title='Software Engineer',
            description='Job description here.',
            location='Remote'
        )

        # Create a dummy resume file
        cls.resume_file = ContentFile(b"This is a dummy resume content.", name='resume.pdf')

    def test_application_creation(self):
        application = Application.objects.create(
            applicant=self.applicant_profile,
            job=self.job,
            resume=self.resume_file,
            cover_letter='My cover letter.',
            status='applied' # Using a value that's not in choices initially to test default later
        )
        application.skills.add(self.skill)  # Add the skill to the application
        self.assertTrue(isinstance(application, Application))
        self.assertEqual(application.applicant, self.applicant_profile)
        self.assertEqual(application.job, self.job)
        self.assertTrue(application.resume.name.startswith('applications/resume')) # Check if it starts with the correct path and original name
        self.assertEqual(application.cover_letter, 'My cover letter.')
        self.assertEqual(application.status, 'applied')
        self.assertIsNotNone(application.application_date)
        self.assertIn(self.skill, application.skills.all())

    def test_application_default_status(self):
        application = Application.objects.create(
            applicant=self.applicant_profile,
            job=self.job,
            resume=self.resume_file,
            cover_letter='My cover letter.',
        )
        self.assertEqual(application.status, 'pending')

    def test_application_unique_together(self):
        Application.objects.create(
            applicant=self.applicant_profile,
            job=self.job,
            resume=self.resume_file,
            cover_letter='First application.'
        )
        with self.assertRaises(Exception): # Catching any exception raised by unique_together
            Application.objects.create(
                applicant=self.applicant_profile,
                job=self.job,
                resume=self.resume_file,
                cover_letter='Second application.'
            )

    def test_application_str_method(self):
        application = Application.objects.create(
            applicant=self.applicant_profile,
            job=self.job,
            resume=self.resume_file,
            cover_letter='My cover letter.'
        )
        expected_str = f"{self.applicant_profile.user.username} applying for {self.job.title}"
        self.assertEqual(str(application), expected_str)

    def test_application_resume_upload_path(self):
        application = Application.objects.create(
            applicant=self.applicant_profile,
            job=self.job,
            resume=self.resume_file,
            cover_letter='My cover letter.'
        )
        self.assertTrue(application.resume.name.startswith('applications/'))

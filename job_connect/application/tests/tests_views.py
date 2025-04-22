from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile, Skill
from recruiter.models import RecruiterProfile
from job.models import Job
from application.models import Application
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class ApplyForJobViewTest(TestCase):
    """
    Tests for the apply_for_job view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the ApplyForJobViewTest.
        """
        # Create a user, applicant profile, recruiter profile, skill, and job for testing
        cls.applicant_user = User.objects.create_user(username='applicant1', password='testpassword')
        cls.applicant_profile = ApplicantProfile.objects.create(
            user=cls.applicant_user,
            headline='Experienced Developer',
            summary='A summary of my skills and experience.'
        )
        cls.skill = Skill.objects.create(name='Python')
        cls.applicant_profile.skills.add(cls.skill)

        # Create a user and recruiter profile for the job
        cls.recruiter_user = User.objects.create_user(username='recruiter1', password='testpassword')
        cls.recruiter_profile = RecruiterProfile.objects.create(  # Correct way to create RecruiterProfile
            user=cls.recruiter_user,
            company_name='Test Corp',
            location='Remote'
        )
        cls.job = Job.objects.create(
            recruiter=cls.recruiter_profile,
            title='Software Engineer',
            description='Job description here.',
            location='Remote'
        )

    def setUp(self):
        """
        Set up the client and URLs for each test.
        """
        self.client = Client()
        self.apply_url = reverse('application:apply_for_job', kwargs={'job_id': self.job.id})
        self.confirmation_url = reverse('application:application_confirmation', kwargs={'job_id': self.job.id})

    def test_apply_for_job_login_required(self):
        """
        Test that the apply_for_job view requires login.
        """
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_apply_for_job_authenticated_applicant_get(self):
        """
        Test that an authenticated applicant can access the apply_for_job view.
        """
        self.client.force_login(self.applicant_user)
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/apply_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['job'], self.job)

    def test_apply_for_job_authenticated_applicant_already_applied(self):
        """
        Test that the apply_for_job view handles the case where an applicant has already applied for the job.
        """
        # Create an existing application
        Application.objects.create(applicant=self.applicant_profile, job=self.job)
        self.client.force_login(self.applicant_user)
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/already_applied.html')
        self.assertEqual(response.context['job'], self.job)

    def test_apply_for_job_authenticated_applicant_post_valid(self):
        """
        Test that an authenticated applicant can successfully submit the application form.
        """
        self.client.force_login(self.applicant_user)
        # Create a dummy resume file
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        post_data = {'resume': resume_file, 'cover_letter': 'My awesome cover letter.'}
        response = self.client.post(self.apply_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.confirmation_url)
        self.assertTrue(Application.objects.filter(applicant=self.applicant_profile, job=self.job).exists())
        application = Application.objects.get(applicant=self.applicant_profile, job=self.job)
        self.assertEqual(application.cover_letter, 'My awesome cover letter.')
        self.assertTrue(application.resume.name.startswith('applications/resume'))

    def test_apply_for_job_authenticated_applicant_post_invalid(self):
        """
        Test that the apply_for_job view handles invalid form submissions.
        """
        self.client.force_login(self.applicant_user)
        post_data = {'cover_letter': 'My awesome cover letter.'} # Missing resume in POST
        files_data = {'resume': None} # Simulate no file uploaded
        response = self.client.post(self.apply_url, post_data, files=files_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/apply_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertIn('resume', response.context['form'].errors) # Ensure there's an error for the resume field
        self.assertFalse(Application.objects.filter(applicant=self.applicant_profile, job=self.job).exists())

    def test_apply_for_job_authenticated_recruiter_get_forbidden(self):
        """
        Test that an authenticated recruiter is forbidden from accessing the apply_for_job view.
        """
        self.client.force_login(self.recruiter_user)
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 403) # Recruiters shouldn't be able to apply

    def test_apply_for_job_authenticated_recruiter_post_forbidden(self):
        """
        Test that an authenticated recruiter is forbidden from submitting the application form.
        """
        self.client.force_login(self.recruiter_user)
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        post_data = {'resume': resume_file, 'cover_letter': 'My awesome cover letter.'}
        response = self.client.post(self.apply_url, post_data, follow=True)
        self.assertEqual(response.status_code, 403)
        # Recruiters shouldn't be able to apply
        self.assertFalse(Application.objects.filter(job=self.job).exists())
        # Just check if any application exists for this job after the recruiter's attempt

class ApplicationConfirmationViewTest(TestCase):
    """
    Tests for the application_confirmation view.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the ApplicationConfirmationViewTest.
        """
        # Create a user, applicant profile, recruiter profile, skill, and job for testing
        cls.recruiter_user = User.objects.create_user(username='recruiter1', password='testpassword')
        cls.recruiter_profile = RecruiterProfile.objects.create(
            user=cls.recruiter_user,
            company_name='Test Corp',
            location='Remote'
        )
        cls.job = Job.objects.create(
            recruiter=cls.recruiter_profile,
            title='Software Engineer',
            description='Job description here.',
            location='Remote'
        )

    def setUp(self):
        """
        Set up the client and URLs for each test.
        """
        self.client = Client()
        self.confirmation_url = reverse('application:application_confirmation', kwargs={'job_id': self.job.id})

    def test_application_confirmation_login_required(self):
        """
        Test that the application_confirmation view requires login.
        """
        response = self.client.get(self.confirmation_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_application_confirmation_authenticated_user_get(self):
        """
        Test that an authenticated user can access the application_confirmation view.
        """
        self.client.force_login(self.recruiter_user) # Any logged-in user should be able to see the confirmation
        response = self.client.get(self.confirmation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/application_confirmation.html')
        self.assertEqual(response.context['job'], self.job)

    def test_application_confirmation_authenticated_applicant_get(self):
        """
        Test that an authenticated applicant can access the application_confirmation view.
        """
        applicant_user = User.objects.create_user(username='applicant1', password='testpassword')
        self.client.force_login(applicant_user)
        response = self.client.get(self.confirmation_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/application_confirmation.html')
        self.assertEqual(response.context['job'], self.job)
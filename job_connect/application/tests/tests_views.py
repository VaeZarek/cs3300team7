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
    @classmethod
    def setUpTestData(cls):
        # Create a user for the applicant
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
        self.client = Client()
        self.apply_url = reverse('application:apply_for_job', kwargs={'job_id': self.job.id})
        self.confirmation_url = reverse('application:application_confirmation', kwargs={'job_id': self.job.id})

    def test_apply_for_job_login_required(self):
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_apply_for_job_authenticated_applicant_get(self):
        self.client.force_login(self.applicant_user)
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/apply_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['job'], self.job)

    def test_apply_for_job_authenticated_applicant_already_applied(self):
        Application.objects.create(applicant=self.applicant_profile, job=self.job)
        self.client.force_login(self.applicant_user)
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/already_applied.html')
        self.assertEqual(response.context['job'], self.job)

    def test_apply_for_job_authenticated_applicant_post_valid(self):
        self.client.force_login(self.applicant_user)
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
        self.client.force_login(self.applicant_user)
        post_data = {'cover_letter': 'My awesome cover letter.'} # Missing resume
        response = self.client.post(self.apply_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application/apply_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertFalse(Application.objects.filter(applicant=self.applicant_profile, job=self.job).exists())

    def test_apply_for_job_authenticated_recruiter_get_forbidden(self):
        self.client.force_login(self.recruiter_user)
        response = self.client.get(self.apply_url)
        self.assertEqual(response.status_code, 403) # Recruiters shouldn't be able to apply

    def test_apply_for_job_authenticated_recruiter_post_forbidden(self):
        self.client.force_login(self.recruiter_user)
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        post_data = {'resume': resume_file, 'cover_letter': 'My awesome cover letter.'}
        response = self.client.post(self.apply_url, post_data, follow=True)
        self.assertEqual(response.status_code, 403) # Recruiters shouldn't be able to apply
        self.assertFalse(Application.objects.filter(applicant=self.recruiter_profile, job=self.job).exists())
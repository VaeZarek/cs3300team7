from django.test import TestCase, Client
from django.urls import reverse
from job.models import Job
from recruiter.models import RecruiterProfile
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
import time


User = get_user_model()

class JobListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpassword')
        recruiter = RecruiterProfile.objects.create(user=user, company_name='Test Corp')
        now = timezone.now()

        Job.objects.create(recruiter=recruiter, title='Job 1', posted_date=now - timedelta(seconds=2))
        time.sleep(0.01)  # Small delay

        Job.objects.create(recruiter=recruiter, title='Job 2', posted_date=now - timedelta(seconds=1))
        time.sleep(0.01)  # Small delay

        Job.objects.create(recruiter=recruiter, title='Job 3', posted_date=now)

    def setUp(self):
        self.client = Client()
        self.list_url = reverse('job:job_list')

    def test_job_list_view_exists(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/job_list.html')

    def test_job_list_displays_all_jobs(self):
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.context['jobs']), 3)
        self.assertContains(response, 'Job 1')
        self.assertContains(response, 'Job 2')
        self.assertContains(response, 'Job 3')

    def test_job_list_is_ordered_by_posted_date_descending(self):
        response = self.client.get(self.list_url)
        jobs = list(response.context['jobs'])
        print(f"\n--- Job Order ---")
        for job in jobs:
            print(f"{job.title}: {job.posted_date}")
        self.assertEqual(jobs[0].title, 'Job 3')
        self.assertEqual(jobs[1].title, 'Job 2')
        self.assertEqual(jobs[2].title, 'Job 1')

class JobDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpassword')
        recruiter = RecruiterProfile.objects.create(user=user, company_name='Test Corp')
        cls.job = Job.objects.create(
            recruiter=recruiter,
            title='Detailed Job',
            description='This is a detailed job description.',
            location='Anywhere'
        )

    def setUp(self):
        self.client = Client()
        self.detail_url = reverse('job:job_detail', kwargs={'pk': self.job.pk})
        self.invalid_detail_url = reverse('job:job_detail', kwargs={'pk': 999}) # An ID that likely doesn't exist

    def test_job_detail_view_exists(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/job_detail.html')

    def test_job_detail_displays_correct_job(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['job'], self.job)
        self.assertContains(response, 'Detailed Job')
        self.assertContains(response, 'This is a detailed job description.')
        self.assertContains(response, 'Anywhere')

    def test_job_detail_returns_404_for_nonexistent_job(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, 404)

class JobCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('job:job_create')
        self.list_url = reverse('job:recruiter_job_list') # Assuming this is where recruiters see their jobs

        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.recruiter = RecruiterProfile.objects.create(user=self.user, company_name='Test Corp')

        self.non_recruiter = User.objects.create_user(username='testapplicant', password='testpassword')

        self.valid_form_data = {
            'title': 'New Job Title',
            'description': 'New Job Description',
            'location': 'New Location',
        }
        self.invalid_form_data = {
            'title': '',  # Missing required field
            'description': 'New Job Description',
            'location': 'New Location',
        }

    def test_job_create_view_login_required(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_job_create_view_recruiter_required(self):
        self.client.force_login(self.non_recruiter)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'recruiter:recruiter_profile_create'))
        # Assuming this URL is in your recruiter app's urls

    def test_job_create_view_get_logged_in_recruiter(self):
        self.client.force_login(self.user)
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/job_form.html')
        self.assertIn('form', response.context)

    def test_job_create_view_post_valid_logged_in_recruiter(self):
        self.client.force_login(self.user)
        response = self.client.post(self.create_url, self.valid_form_data, follow=True)
        self.assertEqual(response.status_code, 200)  # Assuming redirect to recruiter's job list
        self.assertRedirects(response, '/recruiter/jobs/')  # Update the expected URL
        self.assertEqual(Job.objects.count(), 1)
        new_job = Job.objects.first()
        self.assertEqual(new_job.title, 'New Job Title')
        self.assertEqual(new_job.recruiter, self.recruiter)

    def test_job_create_view_post_invalid_logged_in_recruiter(self):
        self.client.force_login(self.user)
        response = self.client.post(self.create_url, self.invalid_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/job_form.html')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
        self.assertEqual(Job.objects.count(), 0)

class JobUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testrecruiter', password='testpassword')
        self.recruiter = RecruiterProfile.objects.create(user=self.user, company_name='Test Corp')
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Original Job Title',
            description='Original Job Description',
            location='Original Location'
        )
        self.update_url = reverse('job:job_update', kwargs={'pk': self.job.pk})
        self.list_url = reverse('job:recruiter_job_list')

        self.non_recruiter = User.objects.create_user(username='testapplicant', password='testpassword')
        self.other_recruiter = User.objects.create_user(username='otherrecruiter', password='testpassword')
        self.other_recruiter_profile = RecruiterProfile.objects.create(user=self.other_recruiter, company_name='Other Corp')
        self.other_job = Job.objects.create(
            recruiter=self.other_recruiter_profile,
            title='Other Job',
            description='Other Description',
            location='Other Location'
        )

        self.valid_form_data = {
            'title': 'Updated Job Title',
            'description': 'Updated Job Description',
            'location': 'Updated Location'
        }
        self.invalid_form_data = {
            'title': '',  # Missing required field
            'description': 'Updated Job Description',
            'location': 'Updated Location'
        }

    def test_job_update_view_login_required(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_job_update_view_recruiter_required(self):
        self.client.force_login(self.non_recruiter)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter:recruiter_profile_create'))

    def test_job_update_view_get_logged_in_recruiter_own_job(self):
        self.client.force_login(self.user)
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'job/job_form.html')
        self.assertIn('form', response.context)
        self.assertEqual(response.context['job'], self.job)
        self.assertEqual(response.context['form'].initial['title'], 'Original Job Title')

    def test_job_update_view_get_logged_in_recruiter_other_job(self):
        self.client.force_login(self.user)
        other_job_update_url = reverse('job:job_update', kwargs={'pk': self.other_job.pk})
        response = self.client.get(other_job_update_url)
        self.assertEqual(response.status_code, 404) # Or potentially 302 depending on your get_queryset

    # Add more test methods below for POST requests (valid and invalid data)
    # and ensure the job is updated correctly and access is restricted.
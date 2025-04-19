from django.test import TestCase, Client
from django.urls import reverse
from job.models import Job
from recruiter.models import RecruiterProfile
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()

class JobListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser', password='testpassword')
        recruiter = RecruiterProfile.objects.create(user=user, company_name='Test Corp')
        now = timezone.now()
        Job.objects.create(recruiter=recruiter, title='Job 1', posted_date=now - timedelta(days=2))
        Job.objects.create(recruiter=recruiter, title='Job 2', posted_date=now - timedelta(days=1))
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
        self.assertEqual(jobs[0].title, 'Job 3')
        self.assertEqual(jobs[1].title, 'Job 2')
        self.assertEqual(jobs[2].title, 'Job 1')

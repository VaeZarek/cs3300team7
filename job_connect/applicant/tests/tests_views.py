from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model  # Import get_user_model
from applicant.models import ApplicantProfile, Experience, Education
from applicant.forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404


User = get_user_model()  # Get your custom User model

class ApplicantDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.client.force_login(self.user)
        self.dashboard_url = reverse('applicant:applicant_dashboard')


    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_authenticated_user_can_access(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_dashboard.html')

class ApplicantProfileUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name='Applicant')

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Existing Headline', summary='Existing Summary')
        self.user.groups.add(Group.objects.get(name='Applicant'))
        self.client.force_login(self.user)
        self.update_url = reverse('applicant:applicant_profile_update')
        self.profile_view_url = reverse('applicant:applicant_profile_view') # Add the profile view URL

    def test_get_request_renders_form(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_update.html')
        self.assertIsInstance(response.context['profile_form'], ApplicantProfileForm)
        self.assertIsInstance(response.context['experience_formset'], ExperienceFormSet)
        self.assertIsInstance(response.context['education_formset'], EducationFormSet)

    def test_post_request_only_profile_form(self):
        post_data = {
            'headline': 'Simple Update',
            'summary': 'Simple Summary',
            'experiences-TOTAL_FORMS': '0',
            'experiences-INITIAL_FORMS': '0',
            'experiences-MIN_NUM_FORMS': '0',
            'experiences-MAX_NUM_FORMS': '1000',
            'educations-TOTAL_FORMS': '0',
            'educations-INITIAL_FORMS': '0',
            'educations-MIN_NUM_FORMS': '0',
            'educations-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(self.update_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, self.profile_view_url)
        self.assertEqual(ApplicantProfile.objects.get(user=self.user).headline, 'Simple Update')

    def test_post_request_updates_profile(self):
        post_data = {
            'headline': 'Updated Headline',
            'summary': 'Updated Summary',
            'skills': [],
            'resume': '',

            'experiences-TOTAL_FORMS': '1',  # Use the plural 'experiences'
            'experiences-INITIAL_FORMS': '0',
            'experiences-MIN_NUM_FORMS': '0',
            'experiences-MAX_NUM_FORMS': '1000',
            'experiences-0-title': 'Software Engineer',
            'experiences-0-company': 'Tech Corp',
            'experiences-0-start_date': '2023-01-01',
            'experiences-0-end_date': '2024-01-01',
            'experiences-0-description': 'Developed key features.',
            'experiences-0-DELETE': False,

            'educations-TOTAL_FORMS': '1',  # Use the plural 'educations'
            'educations-INITIAL_FORMS': '0',
            'educations-MIN_NUM_FORMS': '0',
            'educations-MAX_NUM_FORMS': '1000',
            'educations-0-degree': 'Master of Science',
            'educations-0-institution': 'University X',
            'educations-0-graduation_date': '2022-05-01',
            'educations-0-major': 'Computer Science',
            'educations-0-DELETE': False,
        }
        response = self.client.post(self.update_url, post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.wsgi_request.path, self.profile_view_url)
        self.assertTrue(
            Experience.objects.filter(applicant_profile=self.applicant_profile, title='Software Engineer').exists())
        self.assertTrue(
            Education.objects.filter(applicant_profile=self.applicant_profile, degree='Master of Science').exists())

class ApplicantProfileViewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        self.client.force_login(self.user)
        self.view_url = reverse('applicant:applicant_profile_view')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_get_request_renders_form(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_view.html')
        self.assertEqual(response.context['profile'], self.applicant_profile)

        # You would add more tests for handling experience_formset and education_formset
    # and invalid form submissions here.

class ApplicantProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        self.client.force_login(self.user)
        self.view_url = reverse('applicant:applicant_profile_view')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_authenticated_user_can_view_profile(self):
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_view.html')
        self.assertEqual(response.context['profile'], self.applicant_profile)

    def test_redirect_if_profile_does_not_exist(self):
        # Delete the existing profile
        self.applicant_profile.delete()
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('applicant:applicant_profile_create'))


class ApplicantApplicationsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        self.client.force_login(self.user)
        self.applications_url = reverse('applicant:applicant_applications')
        # Create some dummy applications if needed for testing the list

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url)

    def test_authenticated_user_can_access(self):
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_applications_list.html')
        self.assertIn('applications', response.context)

    def test_handles_no_applicant_profile(self):
        # Delete the existing profile
        self.applicant_profile.delete()
        response = self.client.get(self.applications_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_applications_list.html')
        self.assertIn('applications', response.context)
        self.assertEqual(len(response.context['applications']), 0)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model  # Import get_user_model
from applicant.models import ApplicantProfile, Experience, Education
from applicant.forms import ApplicantProfileForm, ExperienceFormSet, EducationFormSet
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
        self.assertIn(reverse('login'), response.url)

    def test_authenticated_user_can_access(self):
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_dashboard.html')

class ApplicantProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Existing Headline', summary='Existing Summary')
        self.client.force_login(self.user)
        self.update_url = reverse('applicant:applicant_profile_update')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_redirect_if_profile_exists(self):
        ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('applicant:applicant_profile_update'))

    def test_get_request_renders_form(self):
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_create.html')
        self.assertIsInstance(response.context['profile_form'], ApplicantProfileForm)

    def test_post_request_creates_profile(self):
        post_data = {'headline': 'New Headline', 'summary': 'New Summary'}
        response = self.client.post(self.create_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('applicant:applicant_dashboard'))
        self.assertTrue(ApplicantProfile.objects.filter(user=self.user, headline='New Headline').exists())

    def test_post_request_with_invalid_data(self):
        post_data = {'headline': '', 'summary': 'New Summary'} # Missing required headline
        response = self.client.post(self.create_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_create.html')
        self.assertIsInstance(response.context['profile_form'], ApplicantProfileForm)
        self.assertTrue(response.context['profile_form'].errors)
        self.assertFalse(ApplicantProfile.objects.filter(user=self.user, summary='New Summary').exists())

class ApplicantProfileViewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testapplicant', password='testpassword')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        self.client.force_login(self.user)
        self.view_url = reverse('applicant:applicant_profile_view')

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_get_request_renders_form(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_update.html')
        self.assertIsInstance(response.context['profile_form'], ApplicantProfileForm)
        self.assertIsInstance(response.context['experience_formset'], ExperienceFormSet)
        self.assertIsInstance(response.context['education_formset'], EducationFormSet)
        self.assertEqual(response.context['profile_form'].instance, self.applicant_profile)

    def test_post_request_updates_profile(self):
        post_data = {'headline': 'Updated Headline', 'summary': 'Updated Summary'}
        response = self.client.post(self.update_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('applicant:applicant_profile_view'))
        self.applicant_profile.refresh_from_db()
        self.assertEqual(self.applicant_profile.headline, 'Updated Headline')
        self.assertEqual(self.applicant_profile.summary, 'Updated Summary')

    # You would add more tests for handling experience_formset and education_formset
    # and invalid form submissions here.

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
        response = self.client.get(self.view_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

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
        self.assertIn(reverse('login'), response.url)

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
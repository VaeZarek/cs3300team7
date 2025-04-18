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
        self.assertIn(reverse('core:login'), response.url)

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

        # Create existing Experience and Education objects and store them as instance attributes
        self.experience = Experience.objects.create(
            applicant_profile=self.applicant_profile,
            title='Old Title',
            company='Old Company',
            start_date='2022-01-01'
        )
        self.education = Education.objects.create(
            applicant_profile=self.applicant_profile,
            degree='Old Degree',
            institution='Old Institution'
        )

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('core:login'), response.url) # Ensure correct reverse for login

    def test_get_request_renders_form(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_update.html')
        self.assertIsInstance(response.context['form'], ApplicantProfileForm)
        self.assertIsInstance(response.context['experience_formset'], ExperienceFormSet)
        self.assertIsInstance(response.context['education_formset'], EducationFormSet)

    def test_post_request_updates_profile(self):
        post_data = {
            'headline': 'Updated Headline',
            'summary': 'Updated Summary',
            'skills': [],
            'resume': '',

            # Experience Formset (Updating existing)
            'experience-TOTAL_FORMS': '1',
            'experience-INITIAL_FORMS': '1',  # Now 1
            'experience-MIN_NUM_FORMS': '0',
            'experience-MAX_NUM_FORMS': '1000',
            'experience-0-id': self.experience.id,  # Include the ID
            'experience-0-title': 'Updated Engineer',
            'experience-0-company': 'New Corp',
            'experience-0-start_date': '2023-02-01',
            'experience-0-end_date': '2024-02-01',
            'experience-0-description': 'Updated features.',
            'experience-0-DELETE': False,

            # Education Formset (Updating existing)
            'education-TOTAL_FORMS': '1',
            'education-INITIAL_FORMS': '1',  # Now 1
            'education-MIN_NUM_FORMS': '0',
            'education-MAX_NUM_FORMS': '1000',
            'education-0-id': self.education.id,  # Include the ID
            'education-0-degree': 'Updated Master',
            'education-0-institution': 'New University',
            'education-0-graduation_date': '2023-06-01',
            'education-0-major': 'Updated Science',
            'education-0-DELETE': False,
        }
        response = self.client.post(self.update_url, post_data)
        self.assertEqual(response.status_code, 302)  # Expect a redirect

        self.assertEqual(ApplicantProfile.objects.get(user=self.user).headline, 'Updated Headline')
        self.assertEqual(Experience.objects.get(id=self.experience.id).title, 'Updated Engineer')
        self.assertEqual(Education.objects.get(id=self.education.id).degree, 'Updated Master')

    def test_post_request_only_profile_form(self):
        post_data = {
            'headline': 'Simple Update',
            'summary': 'Simple Summary',
        }
        response = self.client.post(self.update_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ApplicantProfile.objects.get(user=self.user).headline, 'Simple Update')


    def test_post_request_with_invalid_data(self):
        post_data = {
            'headline': '', # Invalid data
            'summary': 'Updated Summary',
            'experience-TOTAL_FORMS': '0',
            'experience-INITIAL_FORMS': '0',
            'experience-MIN_NUM_FORMS': '0',
            'experience-MAX_NUM_FORMS': '1000',
            'education-TOTAL_FORMS': '0',
            'education-INITIAL_FORMS': '0',
            'education-MIN_NUM_FORMS': '0',
            'education-MAX_NUM_FORMS': '1000',
        }
        response = self.client.post(self.update_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_update.html')
        self.assertTrue(response.context['form'].errors)


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
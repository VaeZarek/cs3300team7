from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile
from applicant.views import applicant_profile_create, applicant_profile_update, applicant_profile_view, \
    applicant_dashboard
from applicant.forms import ApplicantProfileForm
from unittest.mock import patch

User = get_user_model()


class ApplicantProfileViewTest(TestCase):
    """
    Tests for the applicant profile views (create, update, view, dashboard).

    """

    def setUp(self):
        """
        Set up test data for applicant profile tests.

        """
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword', user_type='applicant')
        self.client.force_login(self.user)  # Use force_login for simplicity

    def test_applicant_profile_create_view_get(self):
        """
        Test that the applicant profile create view returns a 200 status code on GET.

        """
        url = reverse('applicant:applicant_profile_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_create.html')

    def test_applicant_profile_create_view_post_valid(self):
        """
        Test that the applicant profile create view creates a new profile on valid POST.

        """
        url = reverse('applicant:applicant_profile_create')
        form_data = {'headline': 'Test Headline', 'summary': 'Test Summary'}
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(ApplicantProfile.objects.filter(user=self.user).exists())

    def test_applicant_profile_update_view_get(self):
        """
        Test that the applicant profile update view returns a 200 status code on GET.

        """
        ApplicantProfile.objects.create(user=self.user, headline='Initial Headline', summary='Initial Summary')
        url = reverse('applicant:applicant_profile_update')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_update.html')

    def test_applicant_profile_update_view_post_valid(self):
        """
        Test that the applicant profile update view updates an existing profile on valid POST.

        """
        profile = ApplicantProfile.objects.create(user=self.user, headline='Initial Headline',
                                                  summary='Initial Summary')
        url = reverse('applicant:applicant_profile_update')
        form_data = {'headline': 'Updated Headline', 'summary': 'Updated Summary'}
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302)  # Redirect after successful update
        profile.refresh_from_db()
        self.assertEqual(profile.headline, 'Updated Headline')

    def test_applicant_profile_view_get(self):
        """
        Test that the applicant profile view returns a 200 status code on GET.

        """
        ApplicantProfile.objects.create(user=self.user, headline='Test Headline', summary='Test Summary')
        url = reverse('applicant:applicant_profile_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_profile_view.html')

    def test_applicant_dashboard_view_get(self):
        """
        Test that the applicant dashboard view returns a 200 status code on GET.

        """
        ApplicantProfile.objects.create(user=self.user, headline='Test Headline', summary='Test Summary')
        url = reverse('applicant:applicant_dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applicant/applicant_dashboard.html')
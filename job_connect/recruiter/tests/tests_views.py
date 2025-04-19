from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from recruiter.models import RecruiterProfile
from recruiter.forms import RecruiterProfileForm

User = get_user_model()

class RecruiterProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testrecruiter', password='testpassword')

    def test_recruiter_profile_create_view_get_no_profile(self):
        self.client.login(username='testrecruiter', password='testpassword')
        response = self.client.get(reverse('recruiter:recruiter_profile_create'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['profile_form'], RecruiterProfileForm)
        self.assertTemplateUsed(response, 'recruiter/recruiter_profile_create.html')
        self.client.logout() # Logout after the test

    def test_recruiter_profile_create_view_get_has_profile(self):
        self.client.login(username='testrecruiter', password='testpassword')
        RecruiterProfile.objects.create(user=self.user, company_name='Existing Co')
        response = self.client.get(reverse('recruiter:recruiter_profile_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter:recruiter_profile_update'))
        self.client.logout()

    def test_recruiter_profile_create_view_post_valid(self):
        self.client.login(username='testrecruiter', password='testpassword')
        post_data = {
            'company_name': 'New Company',
            'company_website': 'https://newco.com',
            'description': 'A new company.',
            'location': 'Denver, CO'
        }
        response = self.client.post(reverse('recruiter:recruiter_profile_create'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter:recruiter_dashboard'))
        self.assertTrue(RecruiterProfile.objects.filter(user=self.user, company_name='New Company', location='Denver, CO').exists())
        self.client.logout()

    def test_recruiter_profile_create_view_post_invalid(self):
        self.client.login(username='testrecruiter', password='testpassword')
        post_data = {
            'company_name': '',  # Missing required field
            'company_website': 'https://newco.com',
            'description': 'A new company.',
            'location': 'Denver, CO'
        }
        response = self.client.post(reverse('recruiter:recruiter_profile_create'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['profile_form'], RecruiterProfileForm)
        self.assertTrue(response.context['profile_form'].errors)
        self.assertFalse(RecruiterProfile.objects.filter(user=self.user).exists())
        self.client.logout()

    def test_recruiter_profile_update_view_get_has_profile(self):
        self.client.login(username='testrecruiter', password='testpassword')
        RecruiterProfile.objects.create(user=self.user, company_name='Existing Co', location='Colorado Springs')
        response = self.client.get(reverse('recruiter:recruiter_profile_update'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['profile_form'], RecruiterProfileForm)
        self.assertEqual(response.context['profile_form'].initial['company_name'], 'Existing Co')
        self.assertEqual(response.context['profile_form'].initial['location'], 'Colorado Springs')
        self.assertTemplateUsed(response, 'recruiter/recruiter_profile_update.html')
        self.client.logout()

    def test_recruiter_profile_update_view_get_no_profile(self):
        self.client.login(username='testrecruiter', password='testpassword')
        response = self.client.get(reverse('recruiter:recruiter_profile_update'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter:recruiter_profile_create'))
        self.client.logout()

    def test_recruiter_profile_update_view_post_valid(self):
        self.client.login(username='testrecruiter', password='testpassword')
        RecruiterProfile.objects.create(user=self.user, company_name='Old Company', location='Old Location')
        post_data = {
            'company_name': 'Updated Company',
            'company_website': 'https://updatedco.com',
            'description': 'An updated company.',
            'location': 'Boulder, CO'
        }
        response = self.client.post(reverse('recruiter:recruiter_profile_update'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('recruiter:recruiter_profile_view'))
        updated_profile = RecruiterProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.company_name, 'Updated Company')
        self.assertEqual(updated_profile.location, 'Boulder, CO')
        self.client.logout()

    def test_recruiter_profile_update_view_post_invalid(self):
        self.client.login(username='testrecruiter', password='testpassword')
        RecruiterProfile.objects.create(user=self.user, company_name='Old Company', location='Old Location')
        post_data = {
            'company_name': '',  # Missing required field
            'company_website': 'https://updatedco.com',
            'description': 'An updated company.',
            'location': 'Boulder, CO'
        }
        response = self.client.post(reverse('recruiter:recruiter_profile_update'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['profile_form'], RecruiterProfileForm)
        self.assertTrue(response.context['profile_form'].errors)
        old_profile = RecruiterProfile.objects.get(user=self.user)
        self.assertEqual(old_profile.company_name, 'Old Company')
        self.assertEqual(old_profile.location, 'Old Location')
        self.client.logout()

    def test_recruiter_profile_create_view_non_logged_in(self):
        response = self.client.get(reverse('recruiter:recruiter_profile_create'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login') + '?next=' + reverse('recruiter:recruiter_profile_create'))

    def test_recruiter_profile_update_view_non_logged_in(self):
        response = self.client.get(reverse('recruiter:recruiter_profile_update'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('core:login') + '?next=' + reverse('recruiter:recruiter_profile_update'))
from django.test import TestCase
from django.contrib.auth import get_user_model
from recruiter.models import RecruiterProfile

User = get_user_model()

class RecruiterProfileModelTest(TestCase):
    """
    Tests for the RecruiterProfile model.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for RecruiterProfileModelTest.
        """
        cls.user1 = User.objects.create_user(username='testrecruiter1', password='testpassword1')
        cls.user2 = User.objects.create_user(username='testrecruiter2', password='testpassword2')
        cls.recruiter1 = RecruiterProfile.objects.create(
            user=cls.user1,
            company_name='Tech Recruiters Inc.',
            company_website='https://techrecruiters.com',
            description='Leading tech recruitment agency.',
            location='San Francisco, CA'
        )
        cls.recruiter2 = RecruiterProfile.objects.create(
            user=cls.user2,
            company_name='Global Talent Solutions',
            location='New York, NY'
        )

    def test_recruiter_profile_creation(self):
        """
        Test that a recruiter profile is created successfully.
        """
        self.assertEqual(self.recruiter1.user.username, 'testrecruiter1')
        self.assertEqual(self.recruiter1.company_name, 'Tech Recruiters Inc.')
        self.assertEqual(self.recruiter1.company_website, 'https://techrecruiters.com')
        self.assertEqual(self.recruiter1.description, 'Leading tech recruitment agency.')
        self.assertEqual(self.recruiter1.location, 'San Francisco, CA')

        self.assertEqual(self.recruiter2.user.username, 'testrecruiter2')
        self.assertEqual(self.recruiter2.company_name, 'Global Talent Solutions')
        self.assertEqual(self.recruiter2.company_website, '')  # Optional field, can be blank
        self.assertEqual(self.recruiter2.description, '')      # Optional field, can be blank
        self.assertEqual(self.recruiter2.location, 'New York, NY')

    def test_recruiter_profile_str_representation(self):
        """
        Test the __str__ method of the RecruiterProfile model.
        """
        self.assertEqual(str(self.recruiter1), 'Tech Recruiters Inc.')
        self.assertEqual(str(self.recruiter2), 'Global Talent Solutions')

    def test_recruiter_profile_user_relationship(self):
        """
        Test the relationship between the User and RecruiterProfile models.
        """
        user1_profile = self.user1.recruiter_profile
        self.assertEqual(user1_profile, self.recruiter1)
        self.assertEqual(user1_profile.company_name, 'Tech Recruiters Inc.')

        user2_profile = self.user2.recruiter_profile
        self.assertEqual(user2_profile, self.recruiter2)
        self.assertEqual(user2_profile.company_name, 'Global Talent Solutions')

    # You can add a test here to briefly check on_delete=models.CASCADE if needed
    # def test_user_deletion_cascades_to_profile(self):
    #     user = User.objects.create_user(username='deletetest', password='test')
    #     profile = RecruiterProfile.objects.create(user=user, company_name='ToDelete')
    #     self.assertTrue(RecruiterProfile.objects.filter(pk=profile.pk).exists())
    #     user.delete()
    #     self.assertFalse(RecruiterProfile.objects.filter(pk=profile.pk).exists())
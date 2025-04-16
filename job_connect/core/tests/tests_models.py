from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            user_type='applicant'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.user_type, 'applicant')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword',
            email='admin@example.com'
        )
        self.assertEqual(admin_user.username, 'adminuser')
        self.assertTrue(admin_user.check_password('adminpassword'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.user_type, '')  # Default should be empty or handled elsewhere

    def test_is_applicant_method(self):
        applicant = User(username='applicant1', user_type='applicant')
        recruiter = User(username='recruiter1', user_type='recruiter')
        other = User(username='other1', user_type='other')  # Assuming you might have other types

        self.assertTrue(applicant.is_applicant())
        self.assertFalse(recruiter.is_applicant())
        self.assertFalse(other.is_applicant())

    def test_is_recruiter_method(self):
        applicant = User(username='applicant1', user_type='applicant')
        recruiter = User(username='recruiter1', user_type='recruiter')
        other = User(username='other1', user_type='other')  # Assuming you might have other types

        self.assertFalse(applicant.is_recruiter())
        self.assertTrue(recruiter.is_recruiter())
        self.assertFalse(other.is_recruiter())

    def test_user_type_choices(self):
        expected_choices = {('applicant', 'Applicant'), ('recruiter', 'Recruiter')}
        actual_choices = set(User._meta.get_field('user_type').choices)
        self.assertEqual(actual_choices, expected_choices)

    def test_groups_and_permissions_fields(self):
        user = User.objects.create_user(username='permsuser', password='password', user_type='applicant')
        self.assertTrue(hasattr(user, 'groups'))
        self.assertTrue(hasattr(user, 'user_permissions'))
        self.assertEqual(user._meta.get_field('groups').remote_field.name, 'group')
        self.assertEqual(user._meta.get_field('user_permissions').remote_field.name, 'permission')
        self.assertEqual(user._meta.get_field('groups').remote_field.related_name, 'core_user_set')
        self.assertEqual(user._meta.get_field('user_permissions').remote_field.related_name, 'core_user_permissions_set')
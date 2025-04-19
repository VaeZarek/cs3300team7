from django.test import TestCase
from core.models import User
from recruiter.forms import RecruiterProfileForm
from recruiter.models import RecruiterProfile


class RecruiterProfileFormsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testrecruiter', password='testpassword')
        self.recruiter_profile = RecruiterProfile.objects.create(user=self.user)

    def test_recruiter_profile_form(self):
        # Provide valid data based on your form fields
        form_data = {'company_name': 'Test Company', 'company_website': 'https://test.com', 'description': 'Test Description'}
        form = RecruiterProfileForm(data=form_data, instance=self.recruiter_profile) # Pass instance if needed
        print(f"\n--- test_recruiter_profile_form (valid) ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_recruiter_profile_form_invalid(self):
        form_data = {} # Providing no data - all fields are likely required
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_invalid ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())

    def test_recruiter_profile_form_missing_required_fields(self):
        form_data = {'company_website': 'https://test.com', 'description': 'Test Description'}  # Missing 'company_name'
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_missing_required_fields ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_recruiter_profile_form_invalid_website_format(self):
        form_data = {'company_name': 'Test Company', 'company_website': 'not a url', 'description': 'Test Description'}
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_invalid_website_format ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())
        self.assertIn('company_website', form.errors)
        self.assertIn('Enter a valid URL.', form.errors['company_website'])

    def test_recruiter_profile_form_description_max_length(self):
        long_description = 'a' * 501  # Assuming a max_length of 500 in the model
        form_data = {'company_name': 'Test Company', 'company_website': 'https://test.com',
                     'description': long_description}
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_description_max_length ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        # You might want to assert the specific error message related to max_length

    def test_recruiter_profile_form_save(self):
        form_data = {'company_name': 'Saved Company', 'company_website': 'https://saved.com',
                     'description': 'Saved Description', 'location': 'New York'}
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_save ---")
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = self.user
            profile.save()
            self.assertTrue(RecruiterProfile.objects.filter(user=self.user, company_name='Saved Company').exists())
        else:
            print(f"Form errors: {form.errors}")
            self.fail("Form should be valid")

    def test_recruiter_profile_form_update(self):
        initial_data = {'company_name': 'Old Company', 'company_website': 'https://old.com',
                        'description': 'Old Description', 'location': 'Chicago'}
        form = RecruiterProfileForm(instance=self.recruiter_profile, data=initial_data)
        form.save()
        self.recruiter_profile.refresh_from_db()
        self.assertEqual(self.recruiter_profile.company_name, 'Old Company')
        self.assertEqual(self.recruiter_profile.location, 'Chicago')

        updated_data = {'company_name': 'Updated Company', 'company_website': 'https://updated.com',
                        'description': 'Updated Description', 'location': 'Seattle'}
        updated_form = RecruiterProfileForm(instance=self.recruiter_profile, data=updated_data)
        updated_form.save()
        self.recruiter_profile.refresh_from_db()
        self.assertEqual(self.recruiter_profile.company_name, 'Updated Company')
        self.assertEqual(self.recruiter_profile.location, 'Seattle')

    def test_recruiter_profile_form_optional_fields_empty(self):
        form_data = {'company_name': 'Test Company', 'company_website': '', 'description': '', 'location': ''}
        form = RecruiterProfileForm(data=form_data)
        print(f"\n--- test_recruiter_profile_form_optional_fields_empty ---")
        print(f"Is form valid? {form.is_valid()}")
        print(f"Form errors: {form.errors}")
        self.assertTrue(form.is_valid())

    def test_recruiter_profile_form_company_name_max_length(self):
        long_company_name = 'a' * 256
        form_data = {'company_name': long_company_name, 'company_website': 'https://test.com',
                     'description': 'Test Description'}
        form = RecruiterProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('company_name', form.errors)

    def test_recruiter_profile_form_location_max_length(self):
        long_location = 'a' * 256
        form_data = {'company_name': 'Test Company', 'company_website': 'https://test.com',
                     'description': 'Test Description', 'location': long_location}
        form = RecruiterProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('location', form.errors)
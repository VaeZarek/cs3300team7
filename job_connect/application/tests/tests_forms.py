from django.test import TestCase
from application.forms import ApplicationForm, ApplicationStatusForm
from django.core.files.uploadedfile import SimpleUploadedFile

class ApplicationFormTest(TestCase):
    """
    Tests for the ApplicationForm.
    """

    def test_valid_application_form(self):
        """
        Test that a valid ApplicationForm is valid.
        """
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        form_data = {'cover_letter': 'My cover letter.'}
        form_files = {'resume': resume_file}
        form = ApplicationForm(form_data, form_files)
        self.assertTrue(form.is_valid())

    def test_application_form_missing_resume(self):
        """
        Test that an ApplicationForm is invalid when missing a resume.
        """
        form_data = {'cover_letter': 'My cover letter.'}
        form = ApplicationForm(form_data, {})
        self.assertFalse(form.is_valid())
        self.assertIn('resume', form.errors)

    def test_application_form_missing_cover_letter(self):
        """
        Test that an ApplicationForm is valid when missing a cover letter.
        """
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        form_files = {'resume': resume_file}
        form = ApplicationForm({}, form_files)
        self.assertTrue(form.is_valid())
        self.assertNotIn('cover_letter', form.errors)

    def test_application_form_file_handling(self):
        """
        Test that an ApplicationForm handles file uploads correctly.
        """
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        form_data = {'cover_letter': 'My cover letter.'}
        form_files = {'resume': resume_file}
        form = ApplicationForm(form_data, form_files)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['resume'].name, 'resume.pdf')
        self.assertEqual(form.cleaned_data['resume'].size, len(b"dummy content"))

class ApplicationStatusFormTest(TestCase):
    """
    Tests for the ApplicationStatusForm.
    """

    def test_valid_application_status_form(self):
        """
        Test that a valid ApplicationStatusForm is valid.
        """
        valid_status = 'reviewed'
        form_data = {'status': valid_status}
        form = ApplicationStatusForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['status'], valid_status)

    def test_invalid_application_status_form(self):
        """
        Test that an ApplicationStatusForm is invalid with an invalid status.
        """
        invalid_status = 'not_a_status'
        form_data = {'status': invalid_status}
        form = ApplicationStatusForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)


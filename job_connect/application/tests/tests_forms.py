from django.test import TestCase
from application.forms import ApplicationForm, ApplicationStatusForm
from django.core.files.uploadedfile import SimpleUploadedFile

class ApplicationFormTest(TestCase):
    def test_valid_application_form(self):
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        form_data = {'cover_letter': 'My cover letter.'}
        form_files = {'resume': resume_file}
        form = ApplicationForm(form_data, form_files)
        self.assertTrue(form.is_valid())

    def test_application_form_missing_resume(self):
        form_data = {'cover_letter': 'My cover letter.'}
        form = ApplicationForm(form_data, {})
        self.assertFalse(form.is_valid())
        self.assertIn('resume', form.errors)

    def test_application_form_missing_cover_letter(self):
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        form_files = {'resume': resume_file}
        form = ApplicationForm({}, form_files)
        self.assertTrue(form.is_valid())
        self.assertNotIn('cover_letter', form.errors)

    def test_application_form_file_handling(self):
        resume_file = SimpleUploadedFile("resume.pdf", b"dummy content", content_type="application/pdf")
        form_data = {'cover_letter': 'My cover letter.'}
        form_files = {'resume': resume_file}
        form = ApplicationForm(form_data, form_files)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['resume'].name, 'resume.pdf')
        self.assertEqual(form.cleaned_data['resume'].size, len(b"dummy content"))

class ApplicationStatusFormTest(TestCase):
    def test_valid_application_status_form(self):
        valid_status = 'reviewed'
        form_data = {'status': valid_status}
        form = ApplicationStatusForm(form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['status'], valid_status)

    def test_invalid_application_status_form(self):
        invalid_status = 'not_a_status'
        form_data = {'status': invalid_status}
        form = ApplicationStatusForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('status', form.errors)


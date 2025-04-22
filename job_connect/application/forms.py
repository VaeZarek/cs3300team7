from django import forms
from application.models import Application

class ApplicationForm(forms.ModelForm):
    """
    Form for submitting an application.

    Args:
        resume (django.forms.FileField): The resume file to be uploaded. Required.
        cover_letter (django.forms.CharField): The cover letter for the application.
    """
    resume = forms.FileField(required=True)
    class Meta:
        """
        Meta class for the ApplicationForm.
        """
        model = Application
        fields = ['resume', 'cover_letter']

class ApplicationStatusForm(forms.ModelForm):
    """
    Form for updating the status of an application.

    Args:
        status (django.forms.CharField): The new status of the application.
    """

    class Meta:
        """
        Meta class for the ApplicationStatusForm.
        """
        model = Application
        fields = ['status']
        
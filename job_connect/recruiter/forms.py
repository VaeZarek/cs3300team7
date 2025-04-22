from django import forms
from recruiter.models import RecruiterProfile

class RecruiterProfileForm(forms.ModelForm):
    """
    Form for creating and updating Recruiter Profiles.

    Attributes:
        company_name (django.forms.CharField): The name of the company.
        company_website (django.forms.URLField): The website of the company.
        description (django.forms.CharField): A brief description of the company.
        location (django.forms.CharField): The location of the company.
    """

    class Meta:
        """
        Meta class for the RecruiterProfileForm.
        """
        model = RecruiterProfile
        fields = ['company_name', 'company_website', 'description', 'location']
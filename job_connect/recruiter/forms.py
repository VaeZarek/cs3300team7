from django import forms
from recruiter.models import RecruiterProfile

class RecruiterProfileForm(forms.ModelForm):
    class Meta:
        model = RecruiterProfile
        fields = ['company_name', 'company_website', 'description']
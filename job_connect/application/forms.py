from django import forms
from application.models import Application

class ApplicationForm(forms.ModelForm):
    resume = forms.FileField(required=True)
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        
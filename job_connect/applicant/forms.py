from django import forms
from applicant.models import ApplicantProfile, Experience, Education
from django.forms.models import inlineformset_factory

class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model = ApplicantProfile
        fields = ['headline', 'summary', 'skills', 'resume']
        widgets = {
            'skills': forms.CheckboxSelectMultiple, # Or forms.SelectMultiple with a widget
        }

ExperienceFormSet = inlineformset_factory(
    ApplicantProfile,
    Experience,
    fields=('title', 'company', 'start_date', 'end_date', 'description'),
    extra=1,
    can_delete=True,
    widgets={
        'start_date': forms.DateInput(attrs={'type': 'date'}),
        'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
)

EducationFormSet = inlineformset_factory(
    ApplicantProfile,
    Education,
    fields=('degree', 'institution', 'graduation_date', 'major'),
    extra=1,
    can_delete=True,
    widgets={
        'graduation_date': forms.DateInput(attrs={'type': 'date'}),
    }
)

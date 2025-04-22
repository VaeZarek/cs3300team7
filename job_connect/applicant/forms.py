from django import forms
from applicant.models import ApplicantProfile, Experience, Education
from django.forms.models import inlineformset_factory

class ApplicantProfileForm(forms.ModelForm):
    """
        Form for creating or updating an ApplicantProfile.

        Attributes:
            headline (CharField):  A short headline describing the applicant.

            summary (TextField):  A summary of the applicant's background and goals.

            skills (MultipleChoiceField):  The applicant's skills.

            resume (FileField):  The applicant's resume.

        """

    class Meta:
        """
        Metadata for the ApplicantProfileForm.

        """
        model = ApplicantProfile
        fields = ['headline', 'summary', 'skills', 'resume']
        widgets = {
            'skills': forms.CheckboxSelectMultiple, # :no-index: Or forms.SelectMultiple with a widget
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
"""
Inline formset for managing an applicant's work experience.

Based on the Experience model, it allows adding, editing, and deleting
experience entries associated with an ApplicantProfile.
"""

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
"""
Inline formset for managing an applicant's education history.

Based on the Education model, this formset enables adding, updating,
and removing education entries linked to an ApplicantProfile.
"""

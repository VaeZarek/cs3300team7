from django import forms
from job.models import Job

class JobForm(forms.ModelForm):
    is_active = forms.BooleanField(initial=True, required=False)  # Explicitly set initial and not required

    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'salary_range', 'employment_type', 'application_deadline', 'is_active', 'skills_required']
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'skills_required': forms.CheckboxSelectMultiple,
        }
        
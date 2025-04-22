from django import forms
from job.models import Job

class JobForm(forms.ModelForm):
    """
    Form for creating and updating Job postings.

    Args:
        title (django.forms.CharField): The title of the job.
        description (django.forms.CharField): A detailed description of the job.
        requirements (django.forms.CharField): The requirements for the job.
        location (django.forms.CharField): The location of the job.
        salary_range (django.forms.CharField): The salary range for the job.
        employment_type (django.forms.CharField): The type of employment (e.g., full-time, part-time).
        application_deadline (django.forms.DateField): The deadline for applications.
        is_active (django.forms.BooleanField): Whether the job posting is active.
        skills_required (django.forms.ModelMultipleChoiceField): The skills required for the job.
    """
    is_active = forms.BooleanField(initial=True)
    # :no-index: Set initial, and it will be required by default

    class Meta:
        """
        Meta class for the JobForm.
        """
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 'salary_range', 'employment_type', 'application_deadline', 'is_active', 'skills_required']
        widgets = {
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
            'skills_required': forms.CheckboxSelectMultiple,
        }
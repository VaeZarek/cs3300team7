from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group  # Import Group
from core.models import User

class ApplicantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'applicant'
        if commit:
            user.save()
            applicant_group = Group.objects.get(name='Applicant')  # Get Applicant group
            user.groups.add(applicant_group)  # Add user to group
        return user

class RecruiterSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'recruiter'
        if commit:
            user.save()
            recruiter_group = Group.objects.get(name='Recruiter')  # Get Recruiter group
            user.groups.add(recruiter_group)  # Add user to group
        return user
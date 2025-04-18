from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group  # Import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class ApplicantSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'applicant'
        if commit:
            user.save()
        return user

class RecruiterSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'recruiter'
        if commit:
            user.save()
        return user
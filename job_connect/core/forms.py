#from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import User

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
    
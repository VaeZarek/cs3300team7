from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group  # :no-index: Import Group
from django.contrib.auth import get_user_model

User = get_user_model()

class ApplicantSignUpForm(UserCreationForm):
    """
    Form for applicant sign-up, extending Django's UserCreationForm.

    It automatically sets the user_type to 'applicant' upon saving.
    """

    class Meta(UserCreationForm.Meta):
        """
        Meta class specifying the User model.
        """
        model = User

    def save(self, commit=True):
        """
        Saves the form and sets the user_type to 'applicant'.

        Args:
            commit (bool, optional): Whether to immediately save the user to the database. Defaults to True.

        Returns:
            User: The saved User object.
        """
        user = super().save(commit=False)
        user.user_type = 'applicant'
        if commit:
            user.save()
        return user

class RecruiterSignUpForm(UserCreationForm):
    """
    Form for recruiter sign-up, extending Django's UserCreationForm.

    It automatically sets the user_type to 'recruiter' upon saving.
    """

    class Meta(UserCreationForm.Meta):
        """
        Meta class specifying the User model.
        """
        model = User

    def save(self, commit=True):
        """
        Saves the form and sets the user_type to 'recruiter'.

        Args:
            commit (bool, optional): Whether to immediately save the user to the database. Defaults to True.

        Returns:
            User: The saved User object.
        """
        user = super().save(commit=False)
        user.user_type = 'recruiter'
        if commit:
            user.save()
        return user
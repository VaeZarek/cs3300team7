from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Attributes:
        user_type (django.db.models.CharField): Field to differentiate between 'applicant' and 'recruiter' users.
    """
    USER_TYPE_CHOICES = (
        ('applicant', 'Applicant'),
        ('recruiter', 'Recruiter'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="core_user_set",  # :no-index: Add a unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions_set",  # :no-index: Add a unique related_name
        related_query_name="user",
    )

    def is_applicant(self):
        """
        Checks if the user is an applicant.

        Returns:
            bool: True if the user is an applicant, False otherwise.
        """
        return self.user_type == 'applicant'

    def is_recruiter(self):
        """
        Checks if the user is a recruiter.

        Returns:
            bool: True if the user is a recruiter, False otherwise.
        """
        return self.user_type == 'recruiter'

    class Meta:
        """
        Meta class for the User model.
        """
        swappable = 'AUTH_USER_MODEL'  # :no-index: Ensure Django knows to use your custom user model


class BaseModel(models.Model):
    """
    Abstract base model that provides timestamp fields (created_at, updated_at).
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for the BaseModel.
        """
        abstract = True



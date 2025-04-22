from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
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
        related_name="core_user_set",  # Add a unique related_name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="core_user_permissions_set",  # Add a unique related_name
        related_query_name="user",
    )

    def is_applicant(self):
        return self.user_type == 'applicant'

    def is_recruiter(self):
        return self.user_type == 'recruiter'

    class Meta:
        swappable = 'AUTH_USER_MODEL' # Ensure Django knows to use your custom user model

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


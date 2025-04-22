from django.db import models
from django.conf import settings
from core.models import BaseModel

class RecruiterProfile(BaseModel):
    """
    Represents a recruiter's profile.

    :param user: The user associated with the recruiter profile.
    :type user: django.conf.settings.AUTH_USER_MODEL
    :param company_name: The name of the company.
    :type company_name: django.db.models.CharField
    :param company_website: The website of the company.
    :type company_website: django.db.models.URLField
    :param description: A brief description of the company.
    :type description: django.db.models.TextField
    :param location: The location of the company.
    :type location: django.db.models.CharField
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    description = models.TextField(blank=True, max_length=500)  # :no-index: Added max_length
    location = models.CharField(max_length=255, blank=True)  # :no-index: Added location field
    # :no-index: Add other relevant fields like company logo, industry, etc.

    def __str__(self):
        """
        Returns the company name as its string representation.

        Returns:
            str: The company name.
        """
        return self.company_name
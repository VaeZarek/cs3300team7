from django.db import models
from django.conf import settings
from core.models import BaseModel

class RecruiterProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)  # Added location field
    # Add other relevant fields like company logo, industry, etc.

    def __str__(self):
        return self.company_name
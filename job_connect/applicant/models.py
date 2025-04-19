from django.db import models
from django.conf import settings
from core.models import BaseModel


class ApplicantProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applicant_profile')
    headline = models.CharField(max_length=255)
    summary = models.TextField(max_length=255)
    skills = models.ManyToManyField('Skill', blank=True, related_name='applicants')
    experience = models.ManyToManyField('Experience', blank=True)
    education = models.ManyToManyField('Education', blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    # Add other relevant fields like location, contact information, etc.

    def __str__(self):
        return self.user.username


class Skill(BaseModel):
    name = models.CharField(max_length=100, unique=True, db_index=True)  # Unique and indexed for efficiency

    def __str__(self):
        return self.name

class Experience(BaseModel):
    applicant_profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} at {self.company}"

class Education(BaseModel):
    applicant_profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_date = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=255, blank=True)
    # Add fields like GPA, etc.

    def __str__(self):
        return f"{self.degree} from {self.institution}"

from django.db import models
#from django.conf import settings
from core.models import BaseModel
from applicant.models import Skill
from recruiter.models import RecruiterProfile

class Job(BaseModel):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(max_length=100, blank=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    skills_required = models.ManyToManyField(Skill, blank=True, related_name='required_in_jobs')
    def __str__(self):
        return self.title
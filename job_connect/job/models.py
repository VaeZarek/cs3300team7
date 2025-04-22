from django.db import models
#from django.conf import settings
from core.models import BaseModel
from applicant.models import Skill
from recruiter.models import RecruiterProfile

class Job(BaseModel):
    """
    Represents a job posting.

    :param recruiter: The recruiter who posted the job.
    :type recruiter: recruiter.models.RecruiterProfile
    :param title: The title of the job.
    :type title: django.db.models.CharField
    :param description: A detailed description of the job.
    :type description: django.db.models.TextField
    :param requirements: The requirements for the job.
    :type requirements: django.db.models.TextField
    :param location: The location of the job.
    :type location: django.db.models.CharField
    :param salary_range: The salary range for the job.
    :type salary_range: django.db.models.CharField
    :param employment_type: The type of employment (e.g., full-time, part-time).
    :type employment_type: django.db.models.CharField
    :param posted_date: The date when the job was posted.
    :type posted_date: django.db.models.DateTimeField
    :param application_deadline: The deadline for applications.
    :type application_deadline: django.db.models.DateField
    :param is_active: Whether the job posting is active.
    :type is_active: django.db.models.BooleanField
    :param skills_required: The skills required for the job.
    :type skills_required: django.db.models.ManyToManyField
    """
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
        """
        Returns the title of the job as its string representation.

        Returns:
            str: The title of the job.
        """
        return self.title
from django.db import models
#from django.conf import settings
from core.models import BaseModel
from job.models import Job
from applicant.models import ApplicantProfile, Skill

class Application(BaseModel):
    applicant = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='job_postings')
    resume = models.FileField(upload_to='applications/', blank=True, null=True) # Allow re-uploading specific resume
    cover_letter = models.TextField(blank=True)
    status = models.CharField(
        max_length=50,
        choices=(
            ('pending', 'Pending'),
            ('reviewed', 'Reviewed'),
            ('shortlisted', 'Shortlisted'),
            ('interviewing', 'Interviewing'),
            ('offered', 'Offered'),
            ('rejected', 'Rejected'),
        ),
        default='pending'
    )

    class Meta:
        unique_together = ('applicant', 'job') # Prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.user.username} applying for {self.job.title}"
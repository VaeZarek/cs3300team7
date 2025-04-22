from django.db import models
#from django.conf import settings
from core.models import BaseModel
from job.models import Job
from applicant.models import ApplicantProfile, Skill

class Application(BaseModel):
    """
    Represents an application submitted by an applicant for a job.

    Args:
        applicant (applicant.models.ApplicantProfile): The applicant who submitted the application.
        job (job.models.Job): The job being applied for.
        application_date (django.db.models.DateTimeField): The date and time when the application was submitted.
        skills (django.db.models.ManyToManyField): The skills associated with the application.
        resume (django.db.models.FileField): The resume uploaded by the applicant.
        cover_letter (django.db.models.TextField): The cover letter submitted by the applicant.
        status (django.db.models.CharField): The current status of the application (e.g., pending, reviewed, etc.).
    """
    applicant = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='job_postings')
    resume = models.FileField(upload_to='applications/', blank=True, null=True) # :no-index: Allow re-uploading specific resume
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
        """
        Meta class for the Application model.

        Defines unique constraint on applicant and job to prevent duplicate applications.
        """
        unique_together = ('applicant', 'job') # :no-index: Prevent duplicate applications

    def __str__(self):
        """
        Returns a string representation of the application.

        Returns:
            str: A string representing the application.
        """
        return f"{self.applicant.user.username} applying for {self.job.title}"
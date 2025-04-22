from django.db import models
from django.conf import settings
from core.models import BaseModel


class ApplicantProfile(BaseModel):
    """
        Applicant profile model.

        Attributes:
            user (OneToOneField): One-to-one relationship with the User model.
            headline (CharField): Applicant's headline.
            summary (TextField): Applicant's summary.
            skills (ManyToManyField): Many-to-many relationship with the Skill model.
            experience (ManyToManyField): Many-to-many relationship with the Experience model.
            education (ManyToManyField): Many-to-many relationship with the Education model.
            resume (FileField): Applicant's resume file.
        """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applicant_profile')
    headline = models.CharField(max_length=255)
    summary = models.TextField(max_length=255)
    skills = models.ManyToManyField('Skill', blank=True, related_name='applicants')
    experience = models.ManyToManyField('Experience', blank=True)
    education = models.ManyToManyField('Education', blank=True) # :no-index:
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    # :no-index: Add other relevant fields like location, contact information, etc.

    def __str__(self):
        """
        Returns the username of the associated user.
        """
        return self.user.username


class Skill(BaseModel):
    """
    Skill model.

    Attributes:
        name (CharField): Name of the skill.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)

    def __str__(self):
        """
        Returns the name of the skill.
        """
        return self.name

class Experience(BaseModel):
    """
    Experience model.

    Attributes:
        applicant_profile (ForeignKey): Foreign key to the ApplicantProfile model.
        title (CharField): Job title.
        company (CharField): Company name.
        start_date (DateField): Start date of the job.
        end_date (DateField): End date of the job (can be null).
        description (TextField): Job description.
    """
    applicant_profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        """
        Returns a string representation of the experience.
        """
        return f"{self.title} at {self.company}"

class Education(BaseModel):
    """
    Education model.

    Attributes:
        applicant_profile (ForeignKey): Foreign key to the ApplicantProfile model.
        degree (CharField): Degree obtained.
        institution (CharField): Institution name.
        graduation_date (DateField): Graduation date (can be null).
        major (CharField): Major subject.
    """
    applicant_profile = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=255)
    institution = models.CharField(max_length=255)
    graduation_date = models.DateField(null=True, blank=True)
    major = models.CharField(max_length=255, blank=True)
    # :no-index: Add fields like GPA, etc.

    def __str__(self):
        """
        Returns a string representation of the education.

        """
        return f"{self.degree} from {self.institution}"

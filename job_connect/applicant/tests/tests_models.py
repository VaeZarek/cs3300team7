from django.test import TestCase
from django.contrib.auth import get_user_model
from applicant.models import ApplicantProfile, Experience, Education
from django.utils import timezone

User = get_user_model()

class ApplicantProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testapplicant')

    def test_applicant_profile_creation(self):
        profile = ApplicantProfile.objects.create(
            user=self.user,
            headline='Experienced Software Engineer',
            summary='A highly motivated and skilled software engineer.',
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.headline, 'Experienced Software Engineer')
        self.assertEqual(profile.summary, 'A highly motivated and skilled software engineer.')
        self.assertTrue(profile.created_at)
        self.assertTrue(profile.updated_at)
        self.assertEqual(str(profile), 'testapplicant')
        self.assertEqual(profile.skills.count(), 0)
        self.assertEqual(profile.experience.count(), 0)
        self.assertEqual(profile.education.count(), 0)
        self.assertFalse(profile.resume)  # Check if the FieldFile evaluates to False


    def test_applicant_profile_skills_relationship(self):
        profile1 = ApplicantProfile.objects.create(user=self.user, headline='Test 1', summary='Summary 1')
        profile2 = ApplicantProfile.objects.create(user=User.objects.create_user(username='testapplicant2'), headline='Test 2', summary='Summary 2')
        python_skill = ApplicantProfile.objects.create(user=User.objects.create_user(username='python'), headline='Python Skill', summary='A skill')
        django_skill = ApplicantProfile.objects.create(user=User.objects.create_user(username='django'), headline='Django Skill', summary='A skill')

        profile1.skills.add(python_skill)
        profile1.skills.add(django_skill)
        profile2.skills.add(python_skill)

        self.assertEqual(profile1.skills.count(), 2)
        self.assertIn(python_skill, profile1.skills.all())
        self.assertIn(django_skill, profile1.skills.all())

        self.assertEqual(profile2.skills.count(), 1)
        self.assertIn(python_skill, profile2.skills.all())
        self.assertNotIn(django_skill, profile2.skills.all())

        self.assertIn(profile1, python_skill.skilled_applicants.all())
        self.assertIn(profile2, python_skill.skilled_applicants.all())
        self.assertIn(profile1, django_skill.skilled_applicants.all())
        self.assertEqual(django_skill.skilled_applicants.count(), 1)

    def test_applicant_profile_resume_upload(self):
        profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        # For testing FileField, you'd typically use SimpleUploadedFile
        from django.core.files.uploadedfile import SimpleUploadedFile
        resume_file = SimpleUploadedFile("resume.pdf", b"This is a test resume content.", content_type="application/pdf")
        profile.resume = resume_file
        profile.save()
        self.assertTrue(profile.resume)
        self.assertIn("resumes/", profile.resume.name)
        # You might want to further test the file content if needed

class ExperienceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testapplicant')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        self.start_date = timezone.now().date()
        self.end_date = timezone.now().date() + timezone.timedelta(days=365)

    def test_experience_creation(self):
        experience = Experience.objects.create(
            applicant_profile=self.applicant_profile,
            title='Software Engineer',
            company='Tech Corp',
            start_date=self.start_date,
            end_date=self.end_date,
            description='Developed and maintained web applications.',
        )
        self.assertEqual(experience.applicant_profile, self.applicant_profile)
        self.assertEqual(experience.title, 'Software Engineer')
        self.assertEqual(experience.company, 'Tech Corp')
        self.assertEqual(experience.start_date, self.start_date)
        self.assertEqual(experience.end_date, self.end_date)
        self.assertEqual(experience.description, 'Developed and maintained web applications.')
        self.assertTrue(experience.created_at)
        self.assertTrue(experience.updated_at)
        self.assertEqual(str(experience), 'Software Engineer at Tech Corp')

    def test_experience_without_end_date(self):
        experience = Experience.objects.create(
            applicant_profile=self.applicant_profile,
            title='Current Role',
            company='Startup Inc',
            start_date=self.start_date,
            description='Currently working on exciting projects.',
        )
        self.assertEqual(experience.end_date, None)

class EducationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testapplicant')
        self.applicant_profile = ApplicantProfile.objects.create(user=self.user, headline='Test', summary='Summary')
        self.graduation_date = timezone.now().date()

    def test_education_creation(self):
        education = Education.objects.create(
            applicant_profile=self.applicant_profile,
            degree='Master of Science',
            institution='University X',
            graduation_date=self.graduation_date,
            major='Computer Science',
        )
        self.assertEqual(education.applicant_profile, self.applicant_profile)
        self.assertEqual(education.degree, 'Master of Science')
        self.assertEqual(education.institution, 'University X')
        self.assertEqual(education.graduation_date, self.graduation_date)
        self.assertEqual(education.major, 'Computer Science')
        self.assertTrue(education.created_at)
        self.assertTrue(education.updated_at)
        self.assertEqual(str(education), 'Master of Science from University X')

    def test_education_without_graduation_date_and_major(self):
        education = Education.objects.create(
            applicant_profile=self.applicant_profile,
            degree='Bachelor of Arts',
            institution='College Y',
        )
        self.assertEqual(education.graduation_date, None)
        self.assertEqual(education.major, '')

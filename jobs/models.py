from django.db import models
from django.conf import settings

class Job(models.Model):
    CATEGORY_CHOICES = (
        ('WEB', 'Web Development'),
        ('MOBILE', 'Mobile Development'),
        ('DESIGN', 'Design'),
        ('WRITING', 'Writing'),
        ('MARKETING', 'Marketing'),
        ('OTHER', 'Other'),
    )

    JOB_TYPE_CHOICES = (
        ('ONE_TIME', 'One-time Project'),
        ('PART_TIME', 'Part-time'),
        ('FULL_TIME', 'Full-time'),
        ('CONTRACT', 'Contract'),
        ('INTERNSHIP', 'Internship'),
    )

    EXPERIENCE_CHOICES = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('EXPERT', 'Expert'),
    )

    STATUS_CHOICES = (
        ('PUBLISHED', 'Published'),
        ('DRAFT', 'Draft'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    recruiter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posted_jobs')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='WEB')
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='ONE_TIME')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='INTERMEDIATE')
    required_skills = models.TextField(help_text="Comma separated skills")
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PUBLISHED')
    
    # Hiring Preferences
    interview_required = models.BooleanField(default=False)
    assessment_required = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

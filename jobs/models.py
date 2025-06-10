from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# Validator for alphabet-only fields
alphabetic_validator = RegexValidator(r'^[a-zA-Z\s]+$', 'This field only allows alphabets and spaces.')

# File validation function (resume, cover letter)
def validate_file(file):
    if not file.name.lower().endswith(('.pdf', '.doc', '.docx')):
        raise ValidationError("Only PDF, DOC, and DOCX files are allowed.")
    if file.size > 5 * 1024 * 1024:
        raise ValidationError("File size should not exceed 5MB.")

# Image validation function (profile pics)
def validate_image(file):
    if not file.name.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise ValidationError("Only PNG, JPG or JPEG files are allowed.")

# Company model
class Company(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.name

# Job model
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255, validators=[alphabetic_validator])
    description = models.TextField()
    location = models.CharField(max_length=255)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

# User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True, validators=[validate_file])
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, validators=[validate_image])

    EXPERIENCE_CHOICES = [
        ('FRESHER', 'Fresher / Entry-Level'),
        ('MID_LEVEL', 'Mid-Level / Intermediate'),
        ('EXPERIENCED', 'Experienced / Senior'),
    ]
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='FRESHER')
    skills = models.TextField(blank=True, null=True, help_text="Comma separated list of skills")
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Application Model
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()  # Mandatory
    resume = models.FileField(upload_to='applications/resumes/', validators=[validate_file])  # Mandatory
    applied_at = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

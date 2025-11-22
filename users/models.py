from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator

# Create your models here.
class User(AbstractUser):
    # User roles
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employer", "Employer"),
        ("applicant", "Applicant"),
    )
    
    # Extended fields
    email = models.EmailField(unique=True, verbose_name="Email Address")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant', verbose_name="User Role")
    address = models.TextField(blank=True, null=True, verbose_name="Address")
    profile_image = models.ImageField(
        upload_to='profile_images/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        verbose_name="Profile Image"
    )
    is_verified = models.BooleanField(default=False, verbose_name="Email Verified")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.get_role_display()}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_employer(self):
        return self.role == 'employer'

    @property
    def is_applicant(self):
        return self.role == 'applicant'


class AdminProfile(models.Model):
    """
    Admin profile model for system administrators
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Department")
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="Employee ID")
    permissions = models.JSONField(default=dict, verbose_name="Admin Permissions")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Admin Profile"
        verbose_name_plural = "Admin Profiles"

    def __str__(self):
        return f"Admin: {self.user.get_full_name()} - {self.department}"


class EmployerProfile(models.Model):
    """
    Employer profile model for companies and recruiters
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    company_description = models.TextField(blank=True, null=True, verbose_name="Company Description")
    company_website = models.URLField(blank=True, null=True, verbose_name="Company Website")
    company_logo = models.ImageField(
        upload_to='company_logos/', 
        blank=True, 
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        verbose_name="Company Logo"
    )
    industry = models.CharField(max_length=100, blank=True, null=True, verbose_name="Industry")
    company_size = models.CharField(max_length=50, blank=True, null=True, verbose_name="Company Size")
    founded_year = models.IntegerField(blank=True, null=True, verbose_name="Founded Year")
    is_verified_employer = models.BooleanField(default=False, verbose_name="Verified Employer")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Employer Profile"
        verbose_name_plural = "Employer Profiles"

    def __str__(self):
        return f"Employer: {self.company_name} - {self.user.get_full_name()}"


class ApplicantProfile(models.Model):
    """
    Applicant profile model for job seekers
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    
    # Personal Information
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        blank=True, 
        null=True,
        verbose_name="Gender"
    )
    
    # Professional Information
    headline = models.CharField(max_length=255, blank=True, null=True, verbose_name="Professional Headline")
    summary = models.TextField(blank=True, null=True, verbose_name="Professional Summary")
    experience_years = models.IntegerField(default=0, verbose_name="Years of Experience")
    
    # Education
    education_level = models.CharField(
        max_length=50,
        choices=[
            ('high_school', 'High School'),
            ('bachelor', 'Bachelor\'s Degree'),
            ('master', 'Master\'s Degree'),
            ('phd', 'PhD'),
            ('other', 'Other')
        ],
        blank=True,
        null=True,
        verbose_name="Education Level"
    )
    
    # Skills and Preferences
    skills = models.JSONField(default=list, verbose_name="Skills")
    preferred_job_types = models.JSONField(default=list, verbose_name="Preferred Job Types")
    preferred_locations = models.JSONField(default=list, verbose_name="Preferred Locations")
    salary_expectation = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        blank=True, 
        null=True,
        verbose_name="Salary Expectation"
    )
    
    # Social Links
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn Profile")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub Profile")
    portfolio_url = models.URLField(blank=True, null=True, verbose_name="Portfolio URL")
    
    # Status
    is_available_for_work = models.BooleanField(default=True, verbose_name="Available for Work")
    is_verified_applicant = models.BooleanField(default=False, verbose_name="Verified Applicant")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Applicant Profile"
        verbose_name_plural = "Applicant Profiles"

    def __str__(self):
        return f"Applicant: {self.user.get_full_name()} - {self.headline or 'No headline'}"

    @property
    def age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
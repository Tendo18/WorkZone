from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.utils import timezone

User = get_user_model()

# Job Types
JOB_TYPES = (
    ("FullTime", "Full Time"),
    ("PartTime", "Part Time"),
    ("Contract", "Contract"),
    ("Remote", "Remote"),
    ("Hybrid", "Hybrid"),
    ("Internship", "Internship"),
    ("Freelance", "Freelance"),
)

# Experience Levels
EXPERIENCE_LEVELS = (
    ("Entry", "Entry Level"),
    ("Junior", "Junior"),
    ("Mid", "Mid Level"),
    ("Senior", "Senior"),
    ("Lead", "Lead"),
    ("Executive", "Executive"),
)

# Application Status
APPLICATION_STATUS = (
    ("Applied", "Applied"),
    ("Under_Review", "Under Review"),
    ("Shortlisted", "Shortlisted"),
    ("Interview", "Interview"),
    ("Rejected", "Rejected"),
    ("Hired", "Hired"),
    ("Withdrawn", "Withdrawn"),
)

class Job(models.Model):
    """
    Job posting model for employers to create job opportunities
    """
    title = models.CharField(max_length=200, verbose_name="Job Title")
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs', verbose_name="Employer")
    
    # Job Details
    description = models.TextField(verbose_name="Job Description")
    requirements = models.TextField(verbose_name="Job Requirements")
    responsibilities = models.TextField(verbose_name="Job Responsibilities")
    
    # Job Specifications
    job_type = models.CharField(max_length=20, choices=JOB_TYPES, default="FullTime", verbose_name="Job Type")
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, default="Entry", verbose_name="Experience Level")
    
    # Location & Salary
    location = models.CharField(max_length=200, verbose_name="Job Location")
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Minimum Salary")
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Maximum Salary")
    salary_currency = models.CharField(max_length=3, default="USD", verbose_name="Salary Currency")
    
    # Skills & Tags
    required_skills = models.JSONField(default=list, verbose_name="Required Skills")
    preferred_skills = models.JSONField(default=list, verbose_name="Preferred Skills")
    tags = models.JSONField(default=list, verbose_name="Job Tags")
    
    # Application Details
    application_deadline = models.DateTimeField(null=True, blank=True, verbose_name="Application Deadline")
    is_active = models.BooleanField(default=True, verbose_name="Active Job")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Job")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.employer.get_full_name()}"
    
    @property
    def is_expired(self):
        """Check if job application deadline has passed"""
        if self.application_deadline:
            return timezone.now() > self.application_deadline
        return False
    
    @property
    def salary_range(self):
        """Get formatted salary range"""
        if self.salary_min and self.salary_max:
            return f"{self.salary_currency} {self.salary_min:,} - {self.salary_max:,}"
        elif self.salary_min:
            return f"{self.salary_currency} {self.salary_min:,}+"
        elif self.salary_max:
            return f"Up to {self.salary_currency} {self.salary_max:,}"
        return "Salary not specified"

class Resume(models.Model):
    """
    Resume model for job seekers to upload and manage their resumes
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', verbose_name="User")
    title = models.CharField(max_length=200, verbose_name="Resume Title")
    file = models.FileField(
        upload_to='resumes/',
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])],
        verbose_name="Resume File"
    )
    is_primary = models.BooleanField(default=False, verbose_name="Primary Resume")
    is_active = models.BooleanField(default=True, verbose_name="Active Resume")
    
    # Resume Details
    summary = models.TextField(blank=True, null=True, verbose_name="Resume Summary")
    skills = models.JSONField(default=list, verbose_name="Skills Listed")
    experience_years = models.IntegerField(default=0, verbose_name="Years of Experience")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Resume"
        verbose_name_plural = "Resumes"
        ordering = ['-is_primary', '-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        # Ensure only one primary resume per user
        if self.is_primary:
            Resume.objects.filter(user=self.user, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class JobApplication(models.Model):
    """
    Job application model for job seekers to apply for jobs
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications', verbose_name="Job")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications', verbose_name="Applicant")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='applications', verbose_name="Resume Used")
    
    # Application Details
    cover_letter = models.TextField(blank=True, null=True, verbose_name="Cover Letter")
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default="Applied", verbose_name="Application Status")
    
    # Additional Information
    expected_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Expected Salary")
    available_start_date = models.DateField(null=True, blank=True, verbose_name="Available Start Date")
    
    # Employer Notes
    employer_notes = models.TextField(blank=True, null=True, verbose_name="Employer Notes")
    is_shortlisted = models.BooleanField(default=False, verbose_name="Shortlisted")
    
    # Timestamps
    applied_at = models.DateTimeField(auto_now_add=True, verbose_name="Applied At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.applicant.get_full_name()} applied for {self.job.title}"
    
    @property
    def days_since_applied(self):
        """Calculate days since application was submitted"""
        return (timezone.now() - self.applied_at).days

class JobSearch(models.Model):
    """
    Model to track job searches for analytics
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_searches', verbose_name="User")
    query = models.CharField(max_length=500, verbose_name="Search Query")
    filters = models.JSONField(default=dict, verbose_name="Applied Filters")
    results_count = models.IntegerField(default=0, verbose_name="Results Count")
    searched_at = models.DateTimeField(auto_now_add=True, verbose_name="Searched At")
    
    class Meta:
        verbose_name = "Job Search"
        verbose_name_plural = "Job Searches"
        ordering = ['-searched_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} searched: {self.query}"

class JobBookmark(models.Model):
    """
    Model for job seekers to bookmark/save jobs
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_jobs', verbose_name="User")
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='bookmarks', verbose_name="Job")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Bookmarked At")
    
    class Meta:
        verbose_name = "Job Bookmark"
        verbose_name_plural = "Job Bookmarks"
        unique_together = ['user', 'job']  # Prevent duplicate bookmarks
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} bookmarked {self.job.title}"

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#Employer recruiting or shit like that
class Employer(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    description = models.TextField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length = 255)
    image = models.ImageField(upload_to='Employer', null= True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#Employee looking for job 
class Applicants(models.Model):
    name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField()
    phone_no = models.CharField(max_length=20)
    image = models.ImageField(upload_to='Employee', null= True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
#Jobs
JOB_TYPES = [
    ("FullTime", "FullTime"),
    ("Flexible", "Flexible"),
    ("Remote", "Remote"),
    ("Hybrid", "Hybrid"),
    ("Internship", "Internship")
]
class Jobs(models.Model):
    title = models.CharField(max_length=50)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    description = models.TextField()
    location = models.CharField(max_length=255)
    job_Type = models.CharField(max_length=50, choices=JOB_TYPES, default = 'Fulltime')
    image = models.ImageField(upload_to='Jobs', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#job application
class Application(models.Model):
    title = models.CharField(max_length=50)
    applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    description = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

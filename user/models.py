from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('jobseeker', 'Job Seeker'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)   
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="jobseeker")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class JobSeekerProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  skills =models.TextField(blank=True)
  education = models.TextField(blank=True)
  experience = models.TextField(blank=True)
  resume = models.FileField(upload_to='resumes/',blank=True,null=True)
  contact_number = models.CharField(max_length=15, blank=True)

  def __str__(self):
        return f"{self.user.username}'s Profile"
  

class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"
    

class Job(models.Model):
    employer = models.ForeignKey(User, on_delete=models.CASCADE,limit_choices_to={'role': 'employer'})
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'jobseeker'})
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('selected', 'Selected')
    ], default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.jobseeker.username} → {self.job.title}"

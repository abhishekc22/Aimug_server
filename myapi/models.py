from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    

class VerifiedUser(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='verification')
    otp = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email}'s OTP ({self.otp})"
    


class JobApplication(models.Model):
    POSITION_CHOICES = [
        ('WFH', 'Work From Home'),
        ('WFO', 'Work From Office'),
        ('Hybrid', 'Hybrid'),
    ]

    position_name = models.CharField(max_length=100)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    responsibility = models.TextField()
    qualifications = models.TextField()
    job_mode = models.CharField(max_length=6, choices=POSITION_CHOICES)
    vacancy = models.IntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    publish_date = models.DateField()

    def __str__(self):
        return self.position_name
    
class Job_applying(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    Job_application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='applications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f"{self.user.username} applied for {self.Job_application.position_name}"

# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField() 
    image = models.ImageField(upload_to='service_images') 

    def __str__(self):
        return self.title
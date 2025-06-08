from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)    
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    extra_info = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Maintance(models.Model):
    STATUS_CHOICES =[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('rejected','rejected'),
        ('done', 'Done'),
    ]
    tenants = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    issue_type = models.CharField(max_length=100)
    property  = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    date = models.DateField(auto_now_add=True)
    request_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='maintenance_photos/', blank=True, null=True)
    def __str__(self):
        return self.title
        
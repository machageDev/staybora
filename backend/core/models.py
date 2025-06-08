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
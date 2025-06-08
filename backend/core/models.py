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
    
class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name
    
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
        
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name}, {self.region}, {self.county}"
    
class Payment(models.Model):
    STATUS_CHOICES =[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    ]
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    def __str__(self):
        return f"{self.tenant.username} - {self.amount}"
    
class TotalPayment(models.Model):
    tenant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date= models.DateTimeField(auto_now_add=True)
    payment_method= models.CharField(max_length=50,choices=[
        ('cash', 'Cash'),
        ('bank transfer', 'Bank Transfer'),
        ('mpesa','mpesa'),
        ('card','card'),
    ])
    reference_number = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.tenant.username} - KES {self.amount_paid} for {self.property.name}"
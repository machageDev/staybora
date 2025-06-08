from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import Lease
from .utils import send_notification_email

def send_rent_due_reminders():
    reminder_date = now().date() + timedelta(days=3)  # 3 days before due
    leases = Lease.objects.filter(rent_due_date=reminder_date)
    
    for lease in leases:
        tenant_email = lease.tenant.email
        subject = "Rent Payment Due Reminder"
        message = (
            f"Dear {lease.tenant.username},\n\n"
            f"This is a friendly reminder that your rent for property "
            f"{lease.property.name} is due on {lease.rent_due_date}.\n"
            "Please ensure payment is made on time to avoid penalties.\n\n"
            "Thank you!"
        )
        send_notification_email(subject, message, [tenant_email])

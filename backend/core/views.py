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

def notify_maintenance_update(maintenance_request):
    tenant_email = maintenance_request.tenant.email
    subject = f"Update on Maintenance Request #{maintenance_request.id}"
    message = (
        f"Dear {maintenance_request.tenant.username},\n\n"
        f"Your maintenance request for '{maintenance_request.issue_type}' "
        f"at {maintenance_request.property.name} has been updated.\n"
        f"Current status: {maintenance_request.status}\n\n"
        "Thank you for your patience."
    )
    send_notification_email(subject, message, [tenant_email])

from django.shortcuts import render
import random
from django.core.mail import send_mail
from django.conf import settings


from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import Lease
from .utils import send_notification_email


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework import status

def send_rent_due_reminders():
    reminder_date = now().date() + timedelta(days=3)  
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

def send_lease_expiry_alerts():
    alert_date = now().date() + timedelta(days=7)  
    leases = Lease.objects.filter(end_date=alert_date)
    
    for lease in leases:
        tenant_email = lease.tenant.email
        admin_email = 'admin@example.com'  
        
        subject_tenant = "Lease Expiry Reminder"
        message_tenant = (
            f"Dear {lease.tenant.username},\n\n"
            f"Your lease for {lease.property.name} is expiring on {lease.end_date}.\n"
            "Please contact management to renew or discuss next steps.\n\n"
            "Thank you!"
        )
        send_notification_email(subject_tenant, message_tenant, [tenant_email])
        
        subject_admin = "Tenant Lease Expiry Alert"
        message_admin = (
            f"Tenant {lease.tenant.username}'s lease for {lease.property.name} "
            f"is expiring on {lease.end_date}."
        )
        send_notification_email(subject_admin, message_admin, [admin_email])


def notify_admin_new_maintenance_request(maintenance_request):
    admin_email = 'admin@example.com'
    subject = f"New Maintenance Request #{maintenance_request.id}"
    message = (
        f"A new maintenance request has been submitted by {maintenance_request.tenant.username} "
        f"for property {maintenance_request.property.name}.\n"
        f"Issue: {maintenance_request.issue_type}\n"
        f"Description: {maintenance_request.description}\n"
        f"Status: {maintenance_request.status}\n"
    )
    send_notification_email(subject, message, [admin_email])
def notify_admin_new_payment(payment):
    admin_email = 'admin@example.com'
    subject = f"New Payment Received: {payment.amount_paid}"
    message = (
        f"Payment of KES {payment.amount_paid} received from {payment.tenant.username} "
        f"for property {payment.property.name} on {payment.payment_date}.\n"
        f"Payment Method: {payment.payment_method}\n"
        f"Reference: {payment.reference_number}\n"
    )
    send_notification_email(subject, message, [admin_email])
def send_otp_email(user_email, otp):
    subject = "Your OTP Code"
    message = f"Your one-time password (OTP) is: {otp}"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
def generate_otp(length=6):   
    otp = ''.join(str(random.randint(0, 9)) for _ in range(length))
    return otp    


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        import json
# yourapp/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def receive_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        print(f"Received location: {latitude}, {longitude}")
        # Optional: save to DB or do processing

        return JsonResponse({"message": "Location received"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


# myapp/tasks.py

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from email_data.models import EmailData
from coldemail import settings
from .models import EmailSchedule
from django.utils import timezone
from authentication.models import CustomUser

@shared_task(bind=True)
def send_department_emails_now(self, department, subject, content, user_email):
    print(f'Starting task to send emails to {department} department')
    recipients = EmailData.objects.filter(group=department)
    print(f'Found {recipients.count()} recipients in {department} department')
    
    html_message = render_to_string('email_template.html', {'department': department, 'content': content})

    print("html ",html_message)
    from_email = settings.EMAIL_HOST_USER

    for recipient in recipients:
        send_mail(
            subject,
            '',
            from_email,
            [recipient.email],
            html_message=html_message,
            fail_silently=True,  # Fail silently should be False for debugging
        )
        print(f'Email sent to {recipient.email}')

    schedule_time = timezone.now()
    
    # Mencari CustomUser berdasarkan email yang diberikan
    try:
        user = CustomUser.objects.get(email=user_email)
    except CustomUser.DoesNotExist:
        user = None
    
    email_schedule = EmailSchedule(
        department=department,
        subject=subject,
        content=content,
        schedule_time=schedule_time,
        user=user,
        status_sent=True
    )
    email_schedule.save()
    return f"Emails sent to {department} department"

@shared_task(bind=True)
def send_department_emails(self, department, subject, content, id):
    print(f'Starting task to send emails to {department} department')
    recipients = EmailData.objects.filter(group=department)
    print(f'Found {recipients.count()} recipients in {department} department')
    
    html_message = render_to_string('email_template.html', {'department': department, 'content': content})

    print("html ", html_message)
    from_email = settings.EMAIL_HOST_USER

    for recipient in recipients:
        send_mail(
            subject,
            '',
            from_email,
            [recipient.email],
            html_message=html_message,
            fail_silently=True,  # Fail silently should be False for debugging
        )
        print(f'Email sent to {recipient.email}')

    # Update status sent to True for the corresponding EmailSchedule
    email_schedule = EmailSchedule.objects.get(id=id)
    email_schedule.status_sent = True
    email_schedule.save()

    return f"Emails sent to {department} department"
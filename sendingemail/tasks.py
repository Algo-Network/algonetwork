# myapp/tasks.py

import logging
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from email_data.models import EmailData
from coldemail import settings
from .models import EmailSchedule
from django.utils import timezone

@shared_task(bind=True)
def send_department_emails_now(self, department, subject, content):
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
    
    email_schedule = EmailSchedule(
        department=department,
        subject=subject,
        content=content,
        schedule_time=schedule_time
    )
    email_schedule.save()
    print("hasil",email_schedule)
    
    return f"Emails sent to {department} department"

def send_department_emails(self, department, subject, content):
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

    
    return f"Emails sent to {department} department"


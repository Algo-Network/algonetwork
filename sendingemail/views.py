from django.shortcuts import render
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.http import JsonResponse
from datetime import datetime
import pytz  
import json
from django.conf import settings
from .models import EmailSchedule
from .tasks import send_department_emails_now, send_department_emails
from .forms import EmailScheduleForm 

def send_email_now(request, department, subject, content):
    print(content)
    send_department_emails_now.delay(department, subject, content, request.user.email)
    return JsonResponse({'success': True, 'message': 'Email sent successfully'})

from django.utils import timezone

def schedule_email_post(request):
    if request.method == 'POST':
        form = EmailScheduleForm(request.POST)
        
        department = request.POST.get('department')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        schedule_time_str = request.POST.get('schedule_time')
        print(schedule_time_str)
        if not schedule_time_str:
            return send_email_now(request, department, subject, content)
        else:
            try:
                schedule_time = timezone.datetime.fromisoformat(schedule_time_str)
                schedule_time = timezone.make_aware(schedule_time, timezone=timezone.get_current_timezone())  # Make it timezone aware
            except ValueError as e:
                print(f"Error converting schedule_time_str: {e}")
                return JsonResponse({'success': False, 'errors': 'Invalid datetime format'})
            
            # Save EmailSchedule
            email_schedule = EmailSchedule.objects.create(
                department=department,
                subject=subject,
                content=content,
                schedule_time=schedule_time,
                user=request.user
            )


            # Save PeriodicTask
            day_of_week = schedule_time.weekday() + 1
            if day_of_week == 7:
                day_of_week = 0
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=schedule_time.minute,
                hour=schedule_time.hour,
                day_of_month=schedule_time.day,
                month_of_year=schedule_time.month,
                day_of_week=day_of_week
            )
            PeriodicTask.objects.create(
                crontab=schedule,
                name=f"Send email to {department} at {schedule_time}",
                task='sendingemail.tasks.send_department_emails',
                args=json.dumps([department, subject, content, str(email_schedule.id)]),
                expires=schedule_time + timezone.timedelta(minutes=10)
            )
            
            return JsonResponse({'success': True, 'message': 'Email scheduled successfully'})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def schedule_success_view(request):
    return render(request, 'schedule_success.html')



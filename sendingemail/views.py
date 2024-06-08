from django.shortcuts import render
from django.utils import timezone
from django_celery_beat.models import CrontabSchedule, PeriodicTask
from django.http import JsonResponse
from datetime import datetime
import pytz  
import json
from django.conf import settings
from .models import EmailSchedule
from .tasks import send_department_emails_now
from .forms import EmailScheduleForm 

def send_email_now(department, subject, content):
    print(content)
    send_department_emails_now.delay(department, subject, content)
    return JsonResponse({'success': True, 'message': 'Email scheduled successfully'})

def schedule_email_view(request):
    if request.method == 'POST':
        form = EmailScheduleForm(request.POST)
        
        department = request.POST.get('department')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        schedule_time = request.POST.get('schedule_time')
        print(schedule_time)
        if not schedule_time:
            return send_email_now(request, department, subject, content)
        else:
            email_schedule = EmailSchedule(
                department=department,
                subject=subject,
                content=content,
                schedule_time=schedule_time
            )
            email_schedule.save()

            try:
                print(f"Received schedule_time_str: {schedule_time}")
                schedule_time = datetime.fromisoformat(schedule_time)      
                schedule_time = timezone.make_aware(schedule_time, timezone=pytz.timezone(settings.TIME_ZONE))
                print(f"Converted schedule_time: {schedule_time}")
            except ValueError as e:
                print(f"Error converting schedule_time_str: {e}")
                return JsonResponse({'success': False, 'errors': 'Invalid datetime format'})             

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
                args=json.dumps([department, subject, content]),
                expires=schedule_time + timezone.timedelta(minutes=1)
            )
            return JsonResponse({'success': True, 'message': 'Email scheduled successfully'})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def schedule_success_view(request):
    return render(request, 'schedule_success.html')



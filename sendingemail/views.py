# myapp/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .forms import EmailScheduleForm
from .models import EmailSchedule
from .tasks import send_department_emails
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from django.http.response import HttpResponse

def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 5, minute = 5)
    task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"+"2", task='sendingemail.tasks.send_mail_func')#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")



def schedule_email_view(request):
    if request.method == 'POST':
        form = EmailScheduleForm(request.POST)
        if form.is_valid():
            department = form.cleaned_data['department']
            schedule_time = form.cleaned_data['schedule_time']
            
            # Save the schedule to the database
            email_schedule = EmailSchedule(department=department, schedule_time=schedule_time)
            email_schedule.save()

            # Calculate the day of the week (0=Sunday, 6=Saturday)
            day_of_week = schedule_time.weekday() + 1
            if day_of_week == 7:
                day_of_week = 0

            # Schedule the task using Celery Beat
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
                args=json.dumps([department]),
                expires=schedule_time + timezone.timedelta(minutes=1)  # Ensure the task expires shortly after execution
            )

            return redirect('sendingemail:schedule_success')
    else:
        form = EmailScheduleForm()

    return render(request, 'schedule_email.html', {'form': form})

def schedule_success_view(request):
    return render(request, 'schedule_success.html')

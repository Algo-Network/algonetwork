from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from sendingemail.models import EmailSchedule
from django_celery_beat.models import PeriodicTask
from sendingemail.forms import EmailScheduleForm
from django.utils import timezone
import json
import math
@staff_member_required(login_url='/auth/login/')
def home(request):
    return render(request, "email_manager.html")


def format_schedule_time(schedule_time):
    # Format the schedule time as desired, e.g., "DD-MM-YYYY HH:MM:SS"
    return schedule_time.strftime("%d-%m-%Y %H:%M:%S")

from django.core.paginator import Paginator

def get_sent_emails(request):
    sent_emails = EmailSchedule.objects.filter(schedule_time__lte=timezone.now())
    total_emails = sent_emails.count()
    page_size = 10  # Misalnya, Anda menggunakan 10 item per halaman
    total_pages = math.ceil(total_emails / page_size)
    data = {
        'emails': [{'id': email.id, 'subject': email.subject, 'schedule_time': format_schedule_time(email.schedule_time)} for email in sent_emails],
        'total_pages': total_pages
    }
    return JsonResponse(data)

def get_scheduled_emails(request):
    scheduled_emails = EmailSchedule.objects.filter(schedule_time__gt=timezone.now())
    total_emails = scheduled_emails.count()
    page_size = 10  # Misalnya, Anda menggunakan 10 item per halaman
    total_pages = math.ceil(total_emails / page_size)
    data = {
        'emails': [{'id': email.id, 'subject': email.subject, 'schedule_time': format_schedule_time(email.schedule_time)} for email in scheduled_emails],
        'total_pages': total_pages
    }
    return JsonResponse(data)


def get_email_details(request, pk):
    email = get_object_or_404(EmailSchedule, pk=pk)
    print(email.content)
    email_details = {
        'id': str(email.id),
        'department': email.department,
        'subject': email.subject,
        'content': email.content,
        'schedule_time': format_schedule_time(email.schedule_time)
    }
    return JsonResponse(email_details)


def edit_schedule_email_view(request, pk):
    email_schedule = get_object_or_404(EmailSchedule, pk=pk)
    periodic_task = get_object_or_404(PeriodicTask, name=f"Send email to {email_schedule.department} at {format_schedule_time(email_schedule.schedule_time)}")
    
    if request.method == 'POST':
        form = EmailScheduleForm(request.POST, instance=email_schedule)
        
        if form.is_valid():
            email_schedule = form.save(commit=False)
            schedule_time = email_schedule.schedule_time

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

            periodic_task.crontab = schedule
            periodic_task.args = json.dumps([email_schedule.department, email_schedule.subject, email_schedule.content])
            periodic_task.expires = schedule_time + timezone.timedelta(minutes=1)
            periodic_task.save()

            email_schedule.save()
            
            return JsonResponse({'success': True, 'message': 'Email schedule updated successfully'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = EmailScheduleForm(instance=email_schedule)
    
    return render(request, 'edit_schedule_email.html', {'form': form, 'email_schedule': email_schedule})

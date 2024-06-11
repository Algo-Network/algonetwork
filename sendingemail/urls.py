# urls.py
from django.urls import path
from .views import schedule_email_post, schedule_success_view

app_name = 'sendingemail'

urlpatterns = [
    path('schedule-email/', schedule_email_post, name='schedule_email'),
    path('schedule-success/', schedule_success_view, name='schedule_success'),
   
]

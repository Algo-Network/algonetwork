import uuid
from django.db import models
from email_data.models import EmailData
# Create your models here.
# myapp/models.py

class EmailSchedule(models.Model):
    DEPARTMENT_CHOICES = EmailData.DEPARTMENT_CHOICES

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

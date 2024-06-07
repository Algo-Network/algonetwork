import uuid
from django.db import models
from email_data.models import EmailData
from ckeditor.fields import RichTextField

class EmailSchedule(models.Model):
    DEPARTMENT_CHOICES = EmailData.DEPARTMENT_CHOICES

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    subject = models.CharField(max_length=255, null=True)  # Subject is typically a short text
    content = RichTextField(blank=True, null=True)  # Content is rich text
    schedule_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

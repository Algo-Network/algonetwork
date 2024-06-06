# myapp/forms.py

from django import forms
from .models import EmailData

class EmailScheduleForm(forms.Form):
    DEPARTMENT_CHOICES = EmailData.DEPARTMENT_CHOICES
    department = forms.ChoiceField(choices=DEPARTMENT_CHOICES)
    schedule_time = forms.DateTimeField(widget=forms.widgets.DateTimeInput(attrs={'type': 'datetime-local'}))

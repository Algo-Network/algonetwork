# from ckeditor.widgets import CKEditorWidget
# class EmailGeneratorForm(forms.Form):
#     LANG_CHOICES = [('id', 'Bahasa Indonesia'), ('en', 'English')]

#     subject = forms.CharField(max_length=100)
#     sendto = forms.ModelChoiceField(queryset=EmailData.objects.values_list('group', flat=True).distinct())
#     mode = forms.ChoiceField(choices=[('formal', 'Formal'), ('casual', 'Casual'), ('persuasive', 'Persuasive'), ('standard', 'Standard'), ('creative', 'Creative')])
#     max_words = forms.IntegerField()
#     email_detail = forms.CharField(widget=forms.Textarea)
#     language = forms.ChoiceField(choices=LANG_CHOICES)
#     body = forms.CharField(widget=CKEditorWidget())

# class EmailGeneratorForm(forms.Form):
#     response = forms.CharField(widget=CKEditorWidget())


# # forms.py
from django import forms
from .models import EmailSchedule
from ckeditor.widgets import CKEditorWidget

class EmailScheduleForm(forms.ModelForm):
    class Meta:
        model = EmailSchedule
        fields = ['department', 'subject', 'content', 'schedule_time']
        widgets = {
            'schedule_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'content': CKEditorWidget(),
        }

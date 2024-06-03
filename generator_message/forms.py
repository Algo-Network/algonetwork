from django import forms
from email_data.models import EmailData

class EmailGeneratorForm(forms.Form):
    LANG_CHOICES = [('id', 'Bahasa Indonesia'), ('en', 'English')]

    subject = forms.CharField(max_length=100)
    sendto = forms.ModelChoiceField(queryset=EmailData.objects.values_list('group', flat=True).distinct())
    mode = forms.ChoiceField(choices=[('formal', 'Formal'), ('casual', 'Casual'), ('persuasive', 'Persuasive'), ('standard', 'Standard'), ('creative', 'Creative')])
    max_words = forms.IntegerField()
    email_detail = forms.CharField(widget=forms.Textarea)
    language = forms.ChoiceField(choices=LANG_CHOICES)

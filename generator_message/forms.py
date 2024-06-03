from django import forms
from django.forms import ModelForm
from .models import EmailGenerator

class CustomPromptForm(forms.ModelForm):
    subject = forms.CharField()
    send_to = forms.CharField(widget=forms.ChoiceField)
    mode = forms.CharField(widget=forms.ChoiceField)
    max_words = forms.IntegerField()
    email_detail = forms.Textarea()
    prompting_result = forms.Textarea()
    class Meta:
        model = EmailGenerator
        fields =('subject','sendto','mode','max_words','email_detail','prompting_result')

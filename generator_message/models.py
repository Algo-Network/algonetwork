from django.db import models

# Create your models here.
class EmailGenerator(models.Model):
    subject = models.CharField(max_length=255)
    sendto = models.CharField(max_length=10, choices=[
        ('Internal', 'Internal'),
        ('External', 'External')
    ])
    mode = models.CharField(max_length=10, choices=[
        ('Formal', 'Formal'),
        ('Casual', 'Casual'),
        ('Persuasive', 'Persuasive'),
        ('Standard', 'Standard'),
        ('Creative', 'Creative')
    ])
    max_words = models.IntegerField()
    email_detail = models.TextField()
    prompting_result = models.TextField()

    def __str__(self):
        return f"EmailGenerator(subject={self.subject},sendto={self.sendto},mode={self.mode},max_words={self.max_words},email_detail={self.email_detail},prompting_result={self.prompting_result})"
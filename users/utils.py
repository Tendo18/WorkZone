from django.core.mail import send_mail
from django.conf import settings

def send_Email(email):
    subject = 'Welcome to the Job Board'
    body = '''
    Thank you for signing up. We hope you enjoy our service.

    ~ The Job board Team
    '''

    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False
    )
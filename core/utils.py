from typing import Protocol

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def calendar_setup():
    """Shows basic usage of the Google Calendar API.
    """
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def send_account_status_email(request, user):
    site = Site.objects.get_current()
    subject, from_email, to = f'{site.name} account blocked', f'{settings.DEFAULT_FROM_EMAIL}', f'{user.email}'

    if request.is_secure:
        protocol = 'https'
    else:
        protocol = 'http'

    context = {
        'protocol': protocol,
        'site': site,
        'user': user
    }
    html_template = get_template('email/account_status.html')
    plaintext = get_template('email/account_status.txt')
    text_content = plaintext.render(context)
    html_content = html_template.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    
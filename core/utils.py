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

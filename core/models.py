import datetime

from django.contrib.auth import get_user_model
from django.db import models
from googleapiclient.discovery import build

from .utils import calendar_setup

User = get_user_model()

DAYS_OF_WEEK = [
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
]

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# stores workout categories and their description
class WorkoutCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


# gym class table
class GymClass(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        WorkoutCategory, on_delete=models.CASCADE, related_name="gym_classes"
    )
    location = models.CharField(max_length=255)
    day_of_week = models.CharField(max_length=15, choices=DAYS_OF_WEEK)
    description = models.TextField()
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    end_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    trainer = models.ForeignKey(
        User,
        limit_choices_to={"role": "Trainer"},
        on_delete=models.CASCADE,
        related_name="classes_in_charge",
    )
    attendees = models.ManyToManyField(
        User, through="Attendee", related_name="attendance",
    )
    google_calendar_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} by {self.trainer}"

    # the method creates a google calendar event when called
    def create_event(self, trainer_email):

        creds = calendar_setup()

        service = build("calendar", "v3", credentials=creds)

        event = {
            "summary": self.name,
            "location": self.location,
            "description": self.description,
            "start": {
                "dateTime": self.start_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "timeZone": "Africa/Nairobi",
            },
            "end": {
                "dateTime": self.end_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "timeZone": "Africa/Nairobi",
            },
            # "recurrence": ["RRULE:FREQ=DAILY;COUNT=2"],
            "attendees": [{"email": trainer_email}],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        event = (
            service.events()
            .insert(calendarId="primary", body=event)
            .execute()
        )
        session = GymClass.objects.get(id=self.id)
        session.google_calendar_id = event.get("id")
        session.save(update_fields=["google_calendar_id"])

    # updates a google calendar event and appends new attendees whenever called
    def update_event(self, member_email):

        creds = calendar_setup()
        service = build("calendar", "v3", credentials=creds)

        event = (
            service.events()
            .get(calendarId="primary", eventId=self.google_calendar_id)
            .execute()
        )

        attendees = event.get("attendees", [])

        attendees.append({"email": member_email})

        changes = {"attendees": attendees}

        service.events().patch(
            calendarId="primary",
            eventId=self.google_calendar_id,
            sendUpdates="all",
            body=changes,
        ).execute()

    # delete a google calendar event instance when called
    def delete_event(self, event_id):
        creds = calendar_setup()
        service = build("calendar", "v3", credentials=creds)
        service.events().delete(
            calendarId="primary", eventId=event_id, sendUpdates="all"
        ).execute()


# pivot table for many to many relationships
class Attendee(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    gym_class = models.ForeignKey(GymClass, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"#{self.id} {self.member}-{self.gym_class}"

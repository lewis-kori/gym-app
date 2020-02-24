from django.contrib import admin
from .models import Attendee,WorkoutCategory,GymClass

admin.site.register(Attendee)
admin.site.register(GymClass)
admin.site.register(WorkoutCategory)
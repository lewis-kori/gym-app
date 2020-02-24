from django.contrib import admin

from .models import (MemberProfile, NextOfKin, TrainerProfile,
                     TrainerSpecialty, UserAccount)

admin.site.register(UserAccount)
admin.site.register(MemberProfile)
admin.site.register(TrainerProfile)
admin.site.register(TrainerSpecialty)
admin.site.register(NextOfKin)

admin.site.site_header = "gymie admin"
admin.site.site_title = "gymie"

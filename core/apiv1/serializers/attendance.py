from rest_framework.serializers import ModelSerializer, SerializerMethodField
from core.models import Attendee, GymClass, WorkoutCategory


class WorkoutCategoryCountSerializer(ModelSerializer):
    attendance_count = SerializerMethodField()

    class Meta:
        model = WorkoutCategory
        fields = ("name",'attendance_count',)

    def get_attendance_count(self, obj):
        user = self.context.get('request').user
        attendance_count = Attendee.objects.filter(
            member=user, gym_class__category=obj
        ).count()
        return attendance_count


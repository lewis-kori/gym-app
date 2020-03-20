from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    PrimaryKeyRelatedField,
    HiddenField,
    CurrentUserDefault,
    SerializerMethodField,
)
from django.contrib.auth import get_user_model
from core.models import Attendee, GymClass, WorkoutCategory
from users.apiv1.serializers.trainer import TrainerDetailSerializer

User = get_user_model()

# serialize workout categories
class WorkoutCategorySerializer(ModelSerializer):
    class Meta:
        model = WorkoutCategory
        fields = "__all__"


# serialize gym class for list display
class GymClassListSerializer(ModelSerializer):
    # category = PrimaryKeyRelatedField(read_only=True)
    trainer = StringRelatedField(
        default=CurrentUserDefault()
    )
    attendees = StringRelatedField(many=True, read_only=True)
    start_time = SerializerMethodField()
    end_time = SerializerMethodField()

    class Meta:
        model = GymClass
        fields = "__all__"

    def get_start_time(self, instance):
        return instance.start_time.strftime('%a %H:%M')

    def get_end_time(self, instance):
        return instance.end_time.strftime('%a %H:%M')

# serialize gym class for detail display
class GymClassDetailSerializer(ModelSerializer):
    attendees = StringRelatedField(many=True)
    category = WorkoutCategorySerializer(read_only=True)
    trainer = TrainerDetailSerializer(read_only=True)

    class Meta:
        model = GymClass
        fields = "__all__"

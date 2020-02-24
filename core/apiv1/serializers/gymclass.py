from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
    PrimaryKeyRelatedField,
    HiddenField,
    CurrentUserDefault,
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
    trainer = PrimaryKeyRelatedField(
        default=CurrentUserDefault(), queryset=User.objects.all()
    )
    attendees = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = GymClass
        fields = "__all__"


# serialize gym class for detail display
class GymClassDetailSerializer(ModelSerializer):
    attendees = StringRelatedField(many=True)
    category = WorkoutCategorySerializer(read_only=True)
    trainer = TrainerDetailSerializer(read_only=True)

    class Meta:
        model = GymClass
        fields = "__all__"

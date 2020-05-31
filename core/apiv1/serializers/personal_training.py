from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        StringRelatedField)

from users.serializers import CustomUserSerializer

from ...models import PersonalTraining


# create a personal training session
class BookTrainerSerializer(ModelSerializer):
    gym_member = StringRelatedField(default=CurrentUserDefault())

    class Meta:
        model = PersonalTraining
        exclude = (
            "google_calendar_id",
            "created_at",
        )


# trainer/member to view his booked sessions
class AllPersonalBookingSerializer(ModelSerializer):
    gym_member = CustomUserSerializer()
    gym_trainer = CustomUserSerializer()

    class Meta:
        model = PersonalTraining
        fields = "__all__"

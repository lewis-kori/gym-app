from django.contrib.auth import get_user_model
# from django.core.exceptions import Attr
from django.forms import model_to_dict
from rest_framework.serializers import (CurrentUserDefault, HiddenField,
                                        ModelSerializer,
                                        PrimaryKeyRelatedField,
                                        SerializerMethodField,
                                        StringRelatedField)

from core.models import Attendee, GymClass, WorkoutCategory
from users.apiv1.serializers.trainer import (TrainerDetailSerializer,
                                             TrainerProfile)
from users.serializers import CustomUserSerializer

User = get_user_model()

# serialize workout categories
class WorkoutCategorySerializer(ModelSerializer):
    class Meta:
        model = WorkoutCategory
        fields = "__all__"


# serialize gym class for list display
class GymClassListSerializer(ModelSerializer):
    trainer = StringRelatedField(
        default=CurrentUserDefault()
    )
    attendees = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = GymClass
        fields = "__all__"

# serialize gym class for creation endpoint display
class GymClassCreateSerializer(ModelSerializer):
    # category = PrimaryKeyRelatedField(read_only=True)
    trainer = StringRelatedField(
        default=CurrentUserDefault()
    )
    attendees = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = GymClass
        fields = "__all__"

# serialize gym class for detail display
class GymClassDetailSerializer(ModelSerializer):
    attendees = StringRelatedField(many=True)
    category = WorkoutCategorySerializer(read_only=True)
    trainer = CustomUserSerializer(read_only=True)
    current_user_booked = SerializerMethodField()

    class Meta:
        model = GymClass
        fields = "__all__"

    def get_current_user_booked(self, obj):
        user = self.context['request'].user
        if user.is_anonymous == False:
            if obj.attendee_set.filter(member=user).exists():
                return True
        return False
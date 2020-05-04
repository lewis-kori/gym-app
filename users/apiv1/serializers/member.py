from rest_framework.serializers import (
    CurrentUserDefault,
    HiddenField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    StringRelatedField,
)

from users.models import MemberProfile, NextOfKin
from users.serializers import CustomUserSerializer

# serialize member profile for creation
class MemberProfileCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = MemberProfile
        fields = "__all__"


# serialize member's profile
class MemberDetailSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = MemberProfile
        fields = "__all__"


# serialize next of kin
class NextOfKinSerializer(ModelSerializer):
    member = StringRelatedField(read_only=True)
    class Meta:
        model = NextOfKin
        fields = "__all__"
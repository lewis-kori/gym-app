from django.core.exceptions import ObjectDoesNotExist
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import SerializerMethodField


class UserRegistrationSerializer(UserCreateSerializer):
    """
    Override djoser's usercreation class to accomodate abstract user fields
    """

    class Meta(UserCreateSerializer.Meta):
        fields = (
            "first_name",
            "last_name",
            "role",
            "email",
            "phone_number",
            "location",
            'image',
            'password',
        )


class CustomUserSerializer(UserSerializer):
    """
    Override djoser current user serializer to return abstact user fields
    """
    has_profile = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            "id",
            'first_name',
            "role",
            "email",
            "phone_number",
            "location",
            'image',
            "is_superuser",
            "has_profile",
        )

    def get_has_profile(self, obj):
        if obj.role == 'Member':
            # check if the users have profiles associated with them
            try:
                return bool(obj.member_profiles)
            except ObjectDoesNotExist:
                return False

        elif obj.role == 'Trainer':
            try:
                return bool(obj.trainer_profiles)
            except ObjectDoesNotExist:
                return False
        else:
            return None

from djoser.serializers import UserCreateSerializer, UserSerializer

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
    # phone_number = SerializerMethodField()
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
        )
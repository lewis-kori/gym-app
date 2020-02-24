from rest_framework.serializers import (CurrentUserDefault, HiddenField,
                                        ModelSerializer, StringRelatedField)

from users.models import TrainerProfile, TrainerSpecialty
from users.serializers import CustomUserSerializer

# allows creation of the trainer profile
class TrainerCreateSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault()) #review later
    class Meta:
        model = TrainerProfile
        fields = '__all__'

# returns an object of trainer profile with user details
class TrainerDetailSerializer(ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = TrainerProfile
        fields = '__all__'

# highlights the specialties of a trainer
class TrainerSpecialtySerializer(ModelSerializer):
    trainer = StringRelatedField(read_only=True)
    class Meta:
        model = TrainerSpecialty
        fields = '__all__'

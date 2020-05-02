from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from ...apiv1.serializers.trainer import (TrainerCreateSerializer,
                                          TrainerDetailSerializer,
                                          TrainerSpecialtySerializer)
from ...models import TrainerProfile, TrainerSpeciality
from ...serializers import CustomUserSerializer

User = get_user_model()

# returns a list of all Trainers
class TrainerListAPIView(ListAPIView):
    queryset = User.objects.filter(role='Trainer')
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny,]

# creation and update of a trainer's profile
class TrainerAPIView(ModelViewSet):
    permission_classes = [AllowAny,]
    queryset = TrainerProfile.objects.all()
    lookup_field = 'user__id'

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrainerCreateSerializer
        return TrainerDetailSerializer

# retrieves a list of all the trainer's specialties
class TrainerSpecialtyListAPIView(ListAPIView):
    serializer_class = TrainerSpecialtySerializer
    queryset = TrainerSpeciality.objects.all()

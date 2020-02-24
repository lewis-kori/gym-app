from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from users.apiv1.serializers.trainer import (TrainerCreateSerializer,
                                             TrainerDetailSerializer,
                                             TrainerSpecialtySerializer)
from users.models import TrainerProfile, TrainerSpecialty


# creation and update of a trainer's profile
class TrainerAPIView(ModelViewSet):
    queryset = TrainerProfile.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TrainerCreateSerializer
        return TrainerDetailSerializer

# retrieves a list of all the trainer's specialties
class TrainerSpecialtyListAPIView(ListAPIView):
    serializer_class = TrainerSpecialtySerializer

    def get_queryset(self):
        trainer_id = self.kwargs['pk']
        return TrainerSpecialty.objects.filter(trainer__id=trainer_id)

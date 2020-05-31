from rest_framework.generics import CreateAPIView,ListAPIView
from rest_framework.permissions import IsAuthenticated

from ..serializers.personal_training import AllPersonalBookingSerializer,BookTrainerSerializer
from ...models import PersonalTraining

# member request view
class BookingCreateAPIView(CreateAPIView):
    queryset = PersonalTraining.objects.all()
    serializer_class = BookTrainerSerializer
    permission_classes = [IsAuthenticated,]


    # attach logged in user to the trainer field on  creation
    def perform_create(self, serializer):
        member = self.request.user
        serializer.save(gym_member=member)
        # serializer.instance.create_event(trainer.email)
        return serializer

# view history of bookings
class BookingHistoryListAPIView(ListAPIView):
    serializer_class = AllPersonalBookingSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Member':
            return PersonalTraining.objects.filter(gym_member=user)
        else:
            return PersonalTraining.objects.filter(gym_trainer=user)
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import PermissionDenied
from ...models import PersonalTraining
from ..serializers.personal_training import (AllPersonalBookingSerializer,
                                             BookTrainerSerializer)
from django.shortcuts import get_object_or_404


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

# accept personal training request
class AcceptPersonalTrainingAPIView(APIView):
    def post(self, request, **kwargs):
        data = request.data
        user = request.user
        permission_classes = [IsAuthenticated,]
        
        # ensure only a trainer has access to the endpoint
        if user.role != 'Trainer':
            raise PermissionDenied(detail='It appears you are not a trainer')


        # look up the request
        request = get_object_or_404(PersonalTraining,gym_trainer=user,id=data['request_id'])
        
        if data['accept'] == 'true':
            if request.is_accepted:
                raise PermissionDenied(detail='It appears you had already accepted this booking. We appreciate the enthuthiasm.')
            
            request.is_accepted = True
            request.create_booking()
            request.save()
            return Response({"detail":"Confirmation successful."},status=HTTP_200_OK)
        elif data['accept'] == 'false':

            # if the booking had previously been accepted and scheduled by google calendar, delete that instance
            if request.is_accepted and request.google_calendar_id:
                request.cancel_booking()
                request.is_accepted = False
                request.save()
                return Response({"detail":"Member will be notified of your response."},status=HTTP_200_OK)

            # if it hadn't been accepted, send an email notification to the members to reduce anticipation
            request.is_accepted = False
            request.save()
            return Response({"detail":"Member will be notified of your response."},status=HTTP_200_OK)
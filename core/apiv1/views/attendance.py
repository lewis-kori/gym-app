from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from core.apiv1.serializers.attendance import WorkoutCategoryCountSerializer
from core.models import Attendee, GymClass, WorkoutCategory

User = get_user_model()


class BookClassAttendanceAPIView(APIView):
    def post(self, request, **kwargs):
        user = get_object_or_404(User, id=self.request.user.id)
        gym_class = get_object_or_404(GymClass, id=kwargs["pk"])
        attendance = Attendee.objects.create(member=user, gym_class=gym_class)
        attendance_email = attendance.member.email
        gym_class.update_event(attendance_email)
        return Response(
            {"detail": "Class booking has been made successfully.🥳"},
            status=HTTP_201_CREATED,
        )


# retrieve list of all classes attended
class ClassAttendanceListAPIView(ListAPIView):
    queryset = WorkoutCategory.objects.all()
    serializer_class = WorkoutCategoryCountSerializer


# delete class Attendance
class CancelClassBookingAPIView(APIView):
    def post(self, request, **kwargs):
        user = request.user
        data = request.data

        # check to see if user is anonymous
        if user.is_anonymous:
            raise PermissionDenied(
                detail="You must be logged in to perform this action."
            )

        # check to ensure the deleting user is in booking
        booking = get_object_or_404(GymClass, pk=data["class_id"],attendees=user)

        booking.attendees.remove(user)
        booking.save()
        return Response(
            {"detail": "Class Booking has been cancelled."}, status=HTTP_202_ACCEPTED
        )

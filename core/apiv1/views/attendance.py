from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.status import HTTP_201_CREATED

from core.models import Attendee, GymClass, WorkoutCategory

from core.apiv1.serializers.attendance import WorkoutCategoryCountSerializer

User = get_user_model()

class BookClassAttendanceAPIView(APIView):
    def post(self, request, **kwargs):
        user = get_object_or_404(User, id=self.request.user.id)
        gym_class = get_object_or_404(GymClass, id=kwargs['pk'])
        attendance = Attendee.objects.create(member=user,gym_class=gym_class)
        attendance_email = attendance.member.email
        gym_class.update_event(attendance_email)
        return Response({'success': True},status=HTTP_201_CREATED)

# retrieve list of all classes attended
class ClassAttendanceListAPIView(ListAPIView):
    queryset = WorkoutCategory.objects.all()
    serializer_class = WorkoutCategoryCountSerializer
from django.urls import path
from core.apiv1.views.attendance import BookClassAttendanceAPIView, ClassAttendanceListAPIView,CancelClassBookingAPIView

urlpatterns = [
    path('create/<int:pk>/',BookClassAttendanceAPIView.as_view()),
    path('cancel/',CancelClassBookingAPIView.as_view()),
    path('category/',ClassAttendanceListAPIView.as_view()),
]

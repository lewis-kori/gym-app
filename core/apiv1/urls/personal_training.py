from django.urls import path

from ..views.personal_training import (BookingCreateAPIView,
                                       BookingHistoryListAPIView)

app_name = 'personal_training'

urlpatterns = [
    path('create/',BookingCreateAPIView.as_view(),name='book_trainer'),
    path('all/',BookingHistoryListAPIView.as_view(),name='my_personal_training_sessions'),
]

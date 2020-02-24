from django.urls import path
from core.apiv1.views.gymclass import GymClassCreateAPIView,GymClassListAPIView,GymClassDeleteAPIView

urlpatterns = [
    path('create/',GymClassCreateAPIView.as_view()),
    path('all/',GymClassListAPIView.as_view()),
    path('delete/<int:pk>/',GymClassDeleteAPIView.as_view()),
]

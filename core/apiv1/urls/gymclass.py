from django.urls import path
from core.apiv1.views.gymclass import (
    GymClassCreateAPIView,
    GymClassDetailAPIView,
    GymClassListAPIView,
    GymClassDeleteAPIView,
    TrainerGymClassListAPIView,
    WorkoutCategoriesListAPIView,
)

urlpatterns = [
    path("create/", GymClassCreateAPIView.as_view()),
    path("all/", GymClassListAPIView.as_view()),
    path("trainer/<int:trainer_pk>/", TrainerGymClassListAPIView.as_view()),
    path("retrieve/<int:pk>/",GymClassDetailAPIView.as_view()),
    path("delete/<int:pk>/", GymClassDeleteAPIView.as_view()),
    path("categories/",WorkoutCategoriesListAPIView.as_view()),
]

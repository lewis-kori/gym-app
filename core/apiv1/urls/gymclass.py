from django.urls import path
from core.apiv1.views.gymclass import (
    GymClassCreateAPIView,
    GymClassDetailAPIView,
    GymClassListAPIView,
    GymClassDeleteAPIView,
    TrainerGymClassListAPIView,
    WorkoutCategoriesListAPIView,
)

app_name = 'gym_class_api'

urlpatterns = [
    path("create/", GymClassCreateAPIView.as_view(),name='new_class'),
    path("all/", GymClassListAPIView.as_view(), name='all_classes'),
    path("trainer/<int:trainer_pk>/", TrainerGymClassListAPIView.as_view(),name='trainer_classes'),
    path("retrieve/<int:pk>/",GymClassDetailAPIView.as_view(),name='gymclass_details'),
    path("delete/<int:pk>/", GymClassDeleteAPIView.as_view(), name='gymclass_delete'),
    path("categories/",WorkoutCategoriesListAPIView.as_view(), name='workout_categories'),
]

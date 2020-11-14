from django.urls import path

from ..templateviews.trainers import (TrainerDetailTemplateView,
                                      TrainerListTemplateView,
                                      TrainerRegistrationTemplateView)

app_name = 'trainers_dashboard'

urlpatterns = [
    path('', TrainerListTemplateView.as_view(), name='trainers_list'),
    path('details/<int:pk>/',
         TrainerDetailTemplateView.as_view(),
         name='trainer_details'),
    path('registration/',
         TrainerRegistrationTemplateView.as_view(),
         name='add_trainer'),
]

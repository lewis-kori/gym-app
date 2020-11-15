from django.urls import path

from ..templateviews.gym_classes import GymClassDetailView, GymClassListView

app_name = 'classes_dashboard'

urlpatterns = [
    path('', GymClassListView.as_view(), name='all_gym_classes'),
    path('details/<int:pk>/',
         GymClassDetailView.as_view(),
         name='gym_class_details'),
]

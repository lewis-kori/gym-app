from django.urls import path

from ..templateviews.gym_classes import (GymClassCreateView,
                                         GymClassDetailView, GymClassListView,
                                         GymClassDeleteView,
                                         GymClassUpdateView)

app_name = 'classes_dashboard'

urlpatterns = [
    path('', GymClassListView.as_view(), name='all_gym_classes'),
    path('new/', GymClassCreateView.as_view(), name='new_gym_class'),
    path('details/<int:pk>/',
         GymClassDetailView.as_view(),
         name='gym_class_details'),
    path('edit/<int:pk>/',
         GymClassUpdateView.as_view(),
         name='update_gym_class'),
    path('delete/<int:pk>/',
         GymClassDeleteView.as_view(),
         name='delete_gym_class'),
]

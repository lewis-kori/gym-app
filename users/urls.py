from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'users'

urlpatterns = [
    path('trainers/',include('users.apiv1.urls.trainer')),
    path('members/',include('users.apiv1.urls.member')),
]

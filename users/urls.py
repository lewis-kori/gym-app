from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('trainers/',include('users.apiv1.urls.trainer')),
    path('members/',include('users.apiv1.urls.member')),
]

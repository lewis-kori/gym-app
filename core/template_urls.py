from django.urls import include, path

from .views import (IndexTemplateView, UserConfirmSuspend,
                    toggle_user_suspension)

app_name = 'dashboard'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('users/confirm-suspend/<int:pk>/',UserConfirmSuspend.as_view(),name='confirm_suspend'),
    path('users/suspend/<int:pk>/',toggle_user_suspension,name='suspend'),
    path('members/', include('core.templateurls.members')),
    path('trainers/', include('core.templateurls.trainers')),
]

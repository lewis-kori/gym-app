from django.urls import path, include

from .views import IndexTemplateView

app_name = 'dashboard'

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('members/', include('core.templateurls.members')),
    path('trainers/', include('core.templateurls.trainers')),
]

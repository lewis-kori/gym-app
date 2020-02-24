from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.apiv1.views.trainer import TrainerAPIView,TrainerSpecialtyListAPIView

router = DefaultRouter()

router.register('', TrainerAPIView)

urlpatterns = [
    path('',include(router.urls)),
    path('specialties/<int:pk>/',TrainerSpecialtyListAPIView.as_view()),
]

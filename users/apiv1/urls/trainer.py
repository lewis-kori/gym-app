from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ...apiv1.views.trainer import (TrainerAPIView, TrainerListAPIView,
                                    TrainerSpecialtyListAPIView)

router = DefaultRouter()

router.register("", TrainerAPIView)

urlpatterns = [
    path("profiles/", include(router.urls)),
    path("all/", TrainerListAPIView.as_view()),
    path("specialties/", TrainerSpecialtyListAPIView.as_view()),
]

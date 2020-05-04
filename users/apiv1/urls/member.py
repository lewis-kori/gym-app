from django.urls import include, path

from users.apiv1.views.member import (MemberProfileCreateAPIView,
                                      MemberProfileReadUpdateAPIView,
                                      NextOfKinAPIView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('next-of-kin',NextOfKinAPIView)

urlpatterns = [
    path('',include(router.urls)),
    path('create/',MemberProfileCreateAPIView.as_view()),
    path('retrieve/<int:pk>/',MemberProfileReadUpdateAPIView.as_view()),
]
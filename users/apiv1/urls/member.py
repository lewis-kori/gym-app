from django.urls import include, path

from users.apiv1.views.member import (MemberProfileCreateAPIView,
                                      MemberProfileReadUpdateAPIView,
                                      NextOfKinAPIView)
from rest_framework.routers import DefaultRouter

app_name = 'member_api_urls'

router = DefaultRouter()

router.register('next-of-kin',NextOfKinAPIView)

urlpatterns = [
    path('',include(router.urls)),
    path('create/',MemberProfileCreateAPIView.as_view(),name='create_member_profile'),
    path('retrieve/<int:pk>/',MemberProfileReadUpdateAPIView.as_view(),name='member_profile_details'),
]
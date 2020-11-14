from django.urls import path

from ..templateviews.members import (MemberDetailTemplateView,
                                     MemberEditTemplateView,
                                     MemberListTemplateView,
                                     MemberRegistrationTemplateView)

app_name='members_dashboard'

urlpatterns = [
    path("", MemberListTemplateView.as_view(), name="members_list"),
    path("details/<int:pk>/",
         MemberDetailTemplateView.as_view(),
         name="member_details"),
    path("edit/<int:pk>/",
         MemberEditTemplateView.as_view(),
         name="member_edit"),
    path('registration/',
         MemberRegistrationTemplateView.as_view(),
         name='add_member'),
]

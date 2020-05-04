from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from users.apiv1.serializers.member import (
    MemberDetailSerializer,
    MemberProfileCreateSerializer,
    NextOfKinSerializer,
)
from users.models import MemberProfile, NextOfKin


# creation of a member profile's
class MemberProfileCreateAPIView(CreateAPIView):
    serializer_class = MemberProfileCreateSerializer
    queryset = MemberProfile.objects.all()


# update/read member's profile
class MemberProfileReadUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = MemberDetailSerializer

    # get a member's profile from the api
    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return MemberProfile.objects.filter(user__id=user_id)


# create member's next of kin
class NextOfKinAPIView(ModelViewSet):
    serializer_class = NextOfKinSerializer
    queryset = NextOfKin.objects.all()
    # http_method_names =['post','put','delete','options']

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(member=user)
        return serializer.save(member=user)

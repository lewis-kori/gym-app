from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter

from core.apiv1.serializers.gymclass import (
    GymClassListSerializer,
    GymClassDetailSerializer,
)
from core.models import GymClass

class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])
# creation of a gym class. limit creation to a trainer
class GymClassCreateAPIView(CreateAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassListSerializer

    # attach logged in user to the trainer field on  creation
    def perform_create(self, serializer):
        trainer = self.request.user
        serializer.save(trainer=trainer)
        serializer.instance.create_event(trainer.email)
        return serializer


# endpoint for retrieving a list of gym classes
class GymClassListAPIView(ListAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassListSerializer
    permission_classes = [AllowAny,]
    search_fields = ['day_of_week']
    filter_backends = [DynamicSearchFilter,]


# shows gym class Details
class GymClassDetailAPIView(RetrieveUpdateAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassDetailSerializer

class GymClassDeleteAPIView(DestroyAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassListSerializer
    
    def perform_destroy(self, instance):
        instance.delete_event(instance.google_calendar_id)
        return super().perform_destroy(instance)
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import AllowAny

from core.apiv1.serializers.gymclass import (GymClassCreateSerializer,
                                             GymClassDetailSerializer,
                                             GymClassListSerializer, WorkoutCategorySerializer)
from core.models import GymClass, WorkoutCategory


class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist("search_fields", [])



# list all categories
class WorkoutCategoriesListAPIView(ListAPIView):
    queryset = WorkoutCategory.objects.all()
    serializer_class = WorkoutCategorySerializer
    
# creation of a gym class. limit creation to a trainer
class GymClassCreateAPIView(CreateAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassCreateSerializer

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
    permission_classes = [
        AllowAny,
    ]
    search_fields = ["day_of_week"]
    filter_backends = [
        DynamicSearchFilter,
    ]

# endpoint for retrieving a list of gym classes owner by a trainer
class TrainerGymClassListAPIView(ListAPIView):
    
    serializer_class = GymClassListSerializer
    permission_classes = [
        AllowAny,
    ]
    search_fields = ["day_of_week"]
    filter_backends = [
        DynamicSearchFilter,
    ]
    def get_queryset(self):
        trainer_id = self.kwargs["trainer_pk"]
        return GymClass.objects.filter(trainer__id=trainer_id)


# shows gym class Details
class GymClassDetailAPIView(RetrieveUpdateAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassDetailSerializer
    permission_classes = [
        AllowAny,
    ]


class GymClassDeleteAPIView(DestroyAPIView):
    queryset = GymClass.objects.all()
    serializer_class = GymClassListSerializer

    def perform_destroy(self, instance):
        if instance.google_calendar_id:
            instance.delete_event(instance.google_calendar_id)
            return super().perform_destroy(instance)
        return super().perform_destroy(instance)

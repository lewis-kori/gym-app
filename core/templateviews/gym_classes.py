from django.views.generic import DetailView, ListView

from ..mixins import AdminDashBoardMixin
from ..models import GymClass


class GymClassListView(AdminDashBoardMixin, ListView):
    model = GymClass
    template_name = 'dashboard/classes/list.html'
    context_object_name = 'gym_classes'


class GymClassDetailView(AdminDashBoardMixin, DetailView):
    model = GymClass
    template_name = 'dashboard/classes/details.html'‚
    context_object_name = 'gym_class'
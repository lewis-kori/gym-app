from django.urls.base import reverse
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ..mixins import AdminDashBoardMixin
from ..models import GymClass

class GymClassCreateView(AdminDashBoardMixin, CreateView):
    model = GymClass
    template_name = 'dashboard/classes/new.html'
    fields = '__all__'

class GymClassUpdateView(AdminDashBoardMixin, UpdateView):
    model = GymClass
    template_name = 'dashboard/classes/new.html'
    fields = '__all__'

class GymClassListView(AdminDashBoardMixin, ListView):
    model = GymClass
    template_name = 'dashboard/classes/list.html'
    context_object_name = 'gym_classes'


class GymClassDetailView(AdminDashBoardMixin, DetailView):
    model = GymClass
    template_name = 'dashboard/classes/details.html'
    context_object_name = 'gym_class'

class GymClassDeleteView(AdminDashBoardMixin, DeleteView):
    model = GymClass
    template_name = 'dashboard/classes/confirm-delete.html'

    def get_success_url(self) -> str:
        return reverse('dashboard:classes_dashboard:all_gym_classes')
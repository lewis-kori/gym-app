from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

from .mixins import AdminDashBoardMixin
from .models import GymClass, PersonalTraining

User = get_user_model()

# Create your views here.
class IndexTemplateView(AdminDashBoardMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent_members"] = User.objects.filter(
            role='Member').order_by("-id")[0:15]
        context["recent_trainers"] = User.objects.filter(
            role='Trainer').order_by("-id")[0:15]
        context['members_count'] = User.objects.filter(role='Member').count()
        context['trainers_count'] = User.objects.filter(role='Trainer').count()
        context['personal_training_sessions'] = PersonalTraining.objects.filter(is_accepted=True).count()
        context['gym_classes'] = GymClass.objects.all().count()
        return context

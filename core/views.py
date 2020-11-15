from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView

from .mixins import AdminDashBoardMixin, check_rights
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

# accepted an incoming order
@login_required
@user_passes_test(check_rights)
def toggle_user_suspension(request, pk):
    user = User.objects.get(pk=pk)

    user.is_active = not user.is_active

    # put email send here
    
    user.save()
    messages.success(request, "User has been deactivated")
    if user.role == 'Member':
        return HttpResponseRedirect(reverse("dashboard:members_dashboard:member_details",
                            kwargs={"pk": user.id}))
    elif user.role == 'Trainer':
        return HttpResponseRedirect(reverse("dashboard:trainers_dashboard:trainer_details",
                            kwargs={"pk": user.id}))

class UserConfirmSuspend(AdminDashBoardMixin, DetailView):
    model = User
    template_name = 'account/confirm-suspend.html'
    context_object_name = 'user'
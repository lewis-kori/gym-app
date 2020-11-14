from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from ..mixins import AdminDashBoardMixin

User = get_user_model()


# get list of all customers
class MemberListTemplateView(AdminDashBoardMixin, ListView):
    model = User
    template_name = "dashboard/members/list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = User.objects.filter(role="Member").order_by("-id")
        return context


# view details of a member
class MemberRegistrationTemplateView(AdminDashBoardMixin, CreateView):
    model = User
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'location',
        'image',
    ]
    template_name = "dashboard/members/add.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        default_password = get_random_string(7)

        user.set_password(default_password)
        user.role = "Member"

        user.save()

        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy("dashboard:members_dashboard:members_details",
                            kwargs={"pk": self.object.pk})


# retrieve an individual customer specific details
class MemberDetailTemplateView(AdminDashBoardMixin, DetailView):
    model = User
    template_name = "dashboard/members/details.html"
    context_object_name = 'member'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[
            "personal_trainings"] = self.object.member_personal_trainings.all(
            )
        context["gym_classes"] = self.object.attendance.all()
        context["next_of_kins"] = self.object.next_of_kins.all()
        return context


# class customer edit form
class MemberEditTemplateView(AdminDashBoardMixin, UpdateView):
    model = User
    fields = [
        'first_name',
        'last_name',
        'email',
        'phone_number',
        'location',
        'image',
    ]
    template_name = "dashboard/members/add.html"

    def get_success_url(self):
        return reverse_lazy("dashboard:members_dashboard:member_details",
                            kwargs={"pk": self.object.pk})

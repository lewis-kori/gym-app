from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View

# controls who views the dashboard
class AdminDashBoardMixin(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return True
        return False

# function for checking rights of the user so as to secure activate deactivate urls
def check_rights(user):
    return user.is_staff or user.is_superuser
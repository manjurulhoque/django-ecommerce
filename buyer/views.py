from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView

from core.models import Order


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    permission_denied_message = "You are not allowed to view this page"
    model = Order
    context_object_name = "orders"
    template_name = "buyer/dashboard.html"

    def test_func(self):
        return self.request.user.user_type == 'buyer'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, ordered=True)

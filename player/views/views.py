from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class GuardedView(LoginRequiredMixin, View):
    login_url = '/account/login/'
    redirect_field_name = 'redirect_to'

from django.shortcuts import render

from player.views.views import GuardedView


class Index(GuardedView):
    def get(self, request):

        return render(request, 'manage.html')
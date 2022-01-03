from django.shortcuts import render

from player.views.views import GuardedView


class Index(GuardedView):
    @staticmethod
    def get(request):
        return render(request, 'manage/index.html')
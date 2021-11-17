from django.shortcuts import render
from django.views import View
from player.models import Song


# noinspection PyMethodMayBeStatic
class Index(View):
    def get(self, request):
        song_id = request.GET.get('song_id')

        if song_id:
            song_to_play = Song.objects.get(id=song_id)
        else:
            song_to_play = ''

        context = {
            'songs': Song.objects.all(),
            'song_to_play': song_to_play
        }
        return render(request, 'index.html', context)

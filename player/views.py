from pprint import pprint

from django.shortcuts import render

from player.models import Song


def index(request):
    if request.method == 'GET':
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

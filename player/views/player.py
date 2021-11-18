from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from player.models import Song, Playlist


class GuardedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class Index(GuardedView):

    def get(self, request):
        song_id = request.GET.get('song_id', False)
        playlist_id = request.GET.get('playlist_id', False)

        context = {
            'playlists': [p for p in Playlist.objects.all()],
        }
        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id)
                context["playlist"] = playlist
                context["playlists"].insert(0, playlist)
                context["songs"] = playlist.songs.all()
            except Playlist.DoesNotExist:
                return redirect('player')

            if song_id:
                try:
                    context["song_to_play"] = Song.objects.get(id=song_id)
                except Song.DoesNotExist:
                    return redirect('player')

        return render(request, 'index.html', context)


class PlaylistView(GuardedView):

    def get(self, request):
        return render(request, 'index.html')

from django.shortcuts import render, redirect
from django.urls import reverse

from player.forms import PlaylistForm
from player.models import Playlist


def create_playlist(request):
    form = PlaylistForm()

    if request.method == 'POST':
        form = PlaylistForm(request.POST, request.FILES)
        if form.is_valid():
            playlist = form.save()
            return redirect('play_playlist', playlist_id=playlist.id)

    context = {
        'action': reverse('create_playlist'),
        'form': form,
        'button_label': 'Playlist erstellen'
    }
    return render(request, 'generic/form.html', context)


def update_playlist(request, playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    form = PlaylistForm(instance=playlist)

    if request.method == 'POST':
        form = PlaylistForm(request.POST, instance=playlist)
        if form.is_valid():
            playlist = form.save()
            return redirect('play_playlist', playlist_id=playlist.id)
    context = {
        'action': reverse('update_playlist', kwargs={'playlist_id': playlist_id}),
        'form': form,
        'button_label': 'Playlist speichern',
    }
    return render(request, 'generic/form.html', context)

import os
from pprint import pprint

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from player.models import Song, Playlist, Artist


class GuardedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class ReadFile(GuardedView):

    def get(self, request):
        return render(request, 'upload_wizard/read_file.html')


class PreviewFile(GuardedView):

    def post(self, request):
        file = request.FILES['file']
        pprint(file)
        pprint(file.name)
        context = {
            'file': file,
            'file_path': file.temporary_file_path()
        }

        return render(request, 'upload_wizard/preview_file.html', context)


class SavedFile(GuardedView):

    def post(self, request):
        pprint(request.POST)
        form = request.POST

        with open(form["file_path"]) as temp_file:

            song = Song.objects.create(
                title=form["title"],
                length=form["length"],
                audio_file=temp_file,
            )

        # os.remove(form["file_path"])

        (artist, _) = Artist.objects.get_or_create(name=form["artist"])

        song.artists.add(artist)

        context = {
            "song": song
        }

        pprint(song)

        return render(request, 'upload_wizard/saved_file.html', context)

from pprint import pprint

from django.contrib import messages
from tinytag import TinyTag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from player.models import TemporaryFileForm, SongForm, TemporaryFile, Artist, Song


class GuardedView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'


class UploadFile(GuardedView):

    def get(self, request):
        context = {
            'action': reverse('upload_song'),
            'form': TemporaryFileForm(),
            'button_label': 'Datei hochladen',
        }
        return render(request, 'upload/form.html', context)

    def post(self, request):
        temp_file_form = TemporaryFileForm(request.POST, request.FILES)

        if not temp_file_form.is_valid():
            messages.error(request, 'Invalid File Format or File too big (max 500mb)')
            return redirect('upload_song')

        temp_file_instance = temp_file_form.save()
        raw_file_name = str(temp_file_form.files.get('file')).split('.')[0].strip()
        params = f"?temp_file_id={temp_file_instance.id}&raw_file_name={raw_file_name}"
        return redirect(reverse('scan_song') + params)


class ScanFile(GuardedView):

    def get(self, request):
        temp_file_id = request.GET['temp_file_id']
        raw_file_name = request.GET['raw_file_name']

        if not temp_file_id:
            print(f'No temp file query string found. Redirecting to file upload.')
            return redirect('song_upload')

        try:
            file_to_scan = TemporaryFile.objects.get(id=temp_file_id)
        except TemporaryFile.DoesNotExist:
            print(f'Temporary file with id {temp_file_id} does not exist. Redirecting to file upload.')
            return redirect('song_upload')

        mp3_file = TinyTag.get(file_to_scan.file.path)
        title = mp3_file.title or raw_file_name or 'Unbekannter Titel'

        artist, _ = Artist.objects.get_or_create(name=(mp3_file.artist or 'Unbekannter Artist'))

        context = {
            'action': reverse('scan_song'),
            'form': SongForm({
                'title': title,
                'artists': [artist],
            }),
            'hidden_fields': [('temp_file_id', temp_file_id)],
            'button_label': 'Song speichern'
        }
        return render(request, 'upload/form.html', context)

    def post(self, request):
        temp_file_id = request.POST.get('temp_file_id')
        song_to_save = SongForm(request.POST)

        try:
            temp_file = TemporaryFile.objects.get(id=temp_file_id)
        except TemporaryFile.DoesNotExist:
            print(f'Requested nonexistent TemporaryFile with id {temp_file_id}')
            print(f' Redirecting to file upload.')
            return redirect('upload_song')

        if not song_to_save.is_valid():
            pprint('SongForm not valid! Rerendering to correct entries')

            context = {
                'action': reverse('scan_song'),
                'form': song_to_save,
                'temp_file_id': temp_file_id,
                'button_label': 'Song speichern'
            }
            return render(request, 'upload/form.html', context)

        else:
            saved_song = song_to_save.save(commit=False)
            saved_song.audio_file = temp_file.file
            saved_song.duration = TinyTag.get(temp_file.file.path).duration
            saved_song.save()
            temp_file.delete()
            pprint(f'Song {saved_song.title} has been uploaded! Redirecting back to upload_song')
            return redirect('upload_song')

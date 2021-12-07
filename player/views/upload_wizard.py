from pprint import pprint

from tinytag import TinyTag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from player.models import TemporaryFileForm, SongForm, TemporaryFile, Artist


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

        if temp_file_form.is_valid():
            temp_file_instance = temp_file_form.save()
            # pprint(temp_file_instance)
            params = f"?temp_file_id={temp_file_instance.id}"
            return redirect(reverse('scan_song') + params)

        else:
            print('Invalid file uploaded! Redirecting back to song_upload')
            return redirect('upload_song')


class ScanFile(GuardedView):

    def get(self, request):
        # pprint(request.GET)
        temp_file_id = request.GET['temp_file_id']

        if not temp_file_id:
            print(f'No temp file query string found. Redirecting to file upload.')
            return redirect('song_upload')

        try:
            file_to_scan = TemporaryFile.objects.get(id=temp_file_id)
            # pprint(file_to_scan)

            mp3_file = TinyTag.get(file_to_scan.file.path)
            # pprint(mp3_file)

            artist, _ = Artist.objects.get_or_create(name=(mp3_file.artist or 'Unbekannter Artist'))
            # pprint(artist)

            context = {
                'action': reverse('scan_song'),
                'form': SongForm({
                    'title': mp3_file.title or 'Unbekannter Titel',
                    'artists': [artist],
                    'audio_file': file_to_scan
                }),
                'hidden_fields': [('temp_file_id', temp_file_id)],
                'button_label': 'Song speichern'
            }

            return render(request, 'upload/form.html', context)

        except TemporaryFile.DoesNotExist:
            print(f'Temporary file with id {temp_file_id} does not exist. Redirecting to file upload.')
            return redirect('song_upload')

    def post(self, request):
        pprint(request.POST)
        temp_file_id = request.POST.get('temp_file_id')
        song_to_save = SongForm(request.POST)

        pprint(TemporaryFile.objects.first().id)
        pprint(temp_file_id)
        song_to_save.audio_file = TemporaryFile.objects.get(id=temp_file_id).file

        if song_to_save.is_valid():

            saved_song = song_to_save.save()
            # pprint(saved_song)

            pprint(f'Song {saved_song.title} has been uploaded! Redirecting back to song_upload')
            return redirect('upload_song')

        else:
            pprint('Invalid form contents! Rerendering to correct entries')

            context = {
                'action': reverse('scan_song'),
                'form': song_to_save,
                'temp_file_id': temp_file_id,
                'button_label': 'Song speichern'
            }
            return render(request, 'upload/form.html', context)

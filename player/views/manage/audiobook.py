import random
from pprint import pprint

from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag

from audioplayer.settings import MEDIA_ROOT
from player.forms import UpdateAudiobookForm, CreateAudiobookForm
from player.models import Track, User
from player.views.views import GuardedView


class CreateAudiobook(GuardedView):

    @staticmethod
    def get(request):
        context = {
            'form': CreateAudiobookForm(),
        }
        return render(request, 'forms/create-audiobook.html', context)

    @staticmethod
    def post(request):
        # request.upload_handlers = [TemporaryFileUploadHandler(request)]
        form = CreateAudiobookForm(request.POST, request.FILES)

        if not form.is_valid():
            pprint(form.errors)
            context = {
                'action': reverse('create_audiobook'),
                'form': form,
            }
            return render(request, 'forms/create-audiobook.html', context)

        audiobook = form.save(commit=False)

        save_user(request, audiobook)
        save_posted_image_or_default(request, audiobook)
        save_all_posted_tracks(request, audiobook)

        audiobook.save()
        print(audiobook.image.name)

        return redirect('update_audiobook', audiobook_id=audiobook.id)


def save_user(request, audiobook):
    user: User = request.user
    audiobook.user = user


def save_posted_image_or_default(request, audiobook):
    image = request.FILES.get('image', None)
    print(f'image in request: {image}')
    if not image:
        audiobook.image.name = pick_random_default_image_path()
    else:
        audiobook.image = image


def save_all_posted_tracks(request, audiobook):
    audiobook.save()
    files = request.FILES.getlist('new_tracks')
    valid_tracks = [Track(title=file.name, audio_file=file, audiobook=audiobook) for file in files if TinyTag.is_supported(file.name)]
    if len(valid_tracks) < len(files):
        names_of_valid_tracks = [track.audio_file.name for track in valid_tracks]
        invalid_files = [file for file in files if file.name not in names_of_valid_tracks]
        [pprint(f'{file.name} ist kein gültiges Audiofile und wurde übersprungen') for file in invalid_files]
        pprint(f'Es wurden {len(valid_tracks)} Audiodateien hochgeladen und '
               f'{len(invalid_files)} ungültige Dateien übersprungen')

    _tracks = Track.objects.bulk_create(valid_tracks)

    for track in _tracks:
        tag = TinyTag.get(f'{MEDIA_ROOT}/{track.audio_file.name}')

        if tag.title:
            track.title = tag.title
        track.duration = tag.duration

        pprint(f'Song {track.title} has been scanned and uploaded!')

    Track.objects.bulk_update(_tracks, ['title', 'duration'])


def pick_random_default_image_path():
    random.seed()
    value = random.randint(1, 10)
    image_path = f'/default_images/default_img{value}.jpg'
    return image_path


class UpdateAudiobook(GuardedView):

    @staticmethod
    def get(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        if not audiobook:
            return redirect('audiobooks')
        audiobook_form = UpdateAudiobookForm(instance=audiobook)

        context = {
            'form': audiobook_form,
            'audiobook_id': audiobook_id,
            'audiobook': audiobook,
        }
        return render(request, 'forms/update-audiobook.html', context)

    @staticmethod
    def post(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        form = UpdateAudiobookForm(request.POST, request.FILES, instance=audiobook)
        if not form.is_valid():
            pprint(form.errors)
            context = {
                'form': form,
                'audiobook_id': audiobook_id,
            }
            return render(request, 'forms/create-audiobook.html', context)

        form.save()
        return redirect('audiobooks')


class DeleteAudiobook(GuardedView):

    @staticmethod
    def get(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        if not audiobook:
            return redirect('audiobooks')
        context = {
            'audiobook_id': audiobook_id
        }
        return render(request, 'forms/delete-audiobook.html', context)

    @staticmethod
    def post(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        if audiobook:
            audiobook.delete()
        return redirect('audiobooks')


def retrieve_audiobook_if_owned(user, audiobook_id):
    return user.audiobook_set.all().get(id=audiobook_id)

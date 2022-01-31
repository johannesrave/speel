#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""This module contains class based views for create, update and delete audiobook."""
import random
from pprint import pprint

from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from tinytag import TinyTag
from pathlib import Path

from audioplayer.settings import MEDIA_ROOT
from player.forms import CreateAudiobookForm
from player.models import Track
from player.views.views import GuardedView


class CreateAudiobook(GuardedView):

    @staticmethod
    def get(request):
        form = CreateAudiobookForm()
        # form.save(commit=False)
        # form.image.name = pick_random_default_image_path()
        # print(form.initial)
        # form.fields["image"].initial = pick_random_default_image_path()

        random.seed()
        image_id = random.randint(1, 10)

        context = {
            'form': form,
            'image_id': image_id
        }
        return render(request, 'forms/audiobook-create.html', context)

    @staticmethod
    def post(request):
        form = CreateAudiobookForm(request.POST, request.FILES)

        if not form.is_valid():
            pprint(form.errors)
            context = {
                'action': reverse('create_audiobook'),
                'form': form,
            }
            return render(request, 'forms/audiobook-create.html', context)

        audiobook = form.save(commit=False)

        save_user(request, audiobook)
        save_posted_image_or_default(request, audiobook)
        save_all_posted_tracks(request, audiobook)

        audiobook.save()
        print(audiobook.image.name)
        [print(track.title) for track in audiobook.tracks.all()]

        return redirect('update_audiobook', audiobook_id=audiobook.id)


class UpdateAudiobook(GuardedView):

    @staticmethod
    def get(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        if not audiobook:
            return redirect('audiobooks')
        audiobook_form = CreateAudiobookForm(instance=audiobook)

        context = {
            'form': audiobook_form,
            'audiobook_id': audiobook_id,
            'audiobook': audiobook,
        }
        return render(request, 'forms/audiobook-update.html', context)

    @staticmethod
    def post(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        form = CreateAudiobookForm(request.POST, request.FILES, instance=audiobook)
        if not form.is_valid():
            pprint(form.errors)
            context = {
                'form': form,
                'audiobook_id': audiobook_id,
            }
            return render(request, 'forms/audiobook-create.html', context)

        audiobook = form.save(commit=False)

        audiobook.last_track_played = None
        audiobook.last_timestamp_played = None

        audiobook.save()
        # audiobook.tracks.all().delete()
        save_all_posted_tracks(request, audiobook)
        [print(track.title) for track in audiobook.tracks.all()]

        audiobook.save()
        print(audiobook.image.name)

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
        return render(request, 'forms/audiobook-delete.html', context)

    @staticmethod
    def post(request, audiobook_id):
        audiobook = retrieve_audiobook_if_owned(request.user, audiobook_id)
        if audiobook:
            audiobook.delete()
        return redirect('audiobooks')


def save_user(request, audiobook):
    user: User = request.user
    audiobook.user = user


def pick_random_default_image_path():
    random.seed()
    value = random.randint(1, 10)
    image_path = f'/default_images/formatted/default_img{value}.jpg'
    return image_path


def save_posted_image_or_default(request, audiobook):
    image = request.FILES.get('image', None)
    print(f'image in request: {image}')
    if not image:
        default_image_id = request.POST.get("image_id", random.randint(1, 10))
        audiobook.image.name = f'/default_images/formatted/default_img{ default_image_id }.jpg'
    else:
        audiobook.image = image


def save_all_posted_tracks(request, audiobook):
    audiobook.save()
    files = request.FILES.getlist('new_tracks')
    valid_files = [file for file in files if TinyTag.is_supported(file.name)]

    if len(valid_files) == 0:
        return
    tracks = [Track(title=file.name, audio_file=file, audiobook=audiobook) for file in valid_files]

    audiobook.tracks.all().delete()

    [pprint(f'{file.name} is not a valid audiofile and was skipped') for file in files if file not in valid_files]

    _tracks = Track.objects.bulk_create(tracks)

    for track in _tracks:
        tag = TinyTag.get(f'{MEDIA_ROOT}/{track.audio_file.name}')

        if tag.title:
            track.title = tag.title
        track.duration = tag.duration

        pprint(f'Song {track.title} has been scanned and uploaded!')

    Track.objects.bulk_update(_tracks, ['title', 'duration'])


def retrieve_audiobook_if_owned(user, audiobook_id):
    return user.audiobook_set.all().get(id=audiobook_id)

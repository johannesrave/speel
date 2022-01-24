#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""This module contains the class based views for viewing and editing the audiobook library."""
from django.shortcuts import render

from player.models import Audiobook
from player.views.views import GuardedView


class ViewLibrary(GuardedView):

    @staticmethod
    def get(request):
        audiobooks = Audiobook.objects.filter(user=request.user)
        context = {'audiobooks': audiobooks}
        return render(request, 'pages/library.html', context)


class EditLibrary(GuardedView):

    @staticmethod
    def get(request):
        audiobooks = Audiobook.objects.filter(user=request.user)
        context = {'audiobooks': audiobooks}
        return render(request, 'pages/audiobooks.html', context)

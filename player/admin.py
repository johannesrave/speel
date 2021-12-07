from django.contrib import admin
from django.apps import apps
from player.models import Playlist, Song, Album, Artist, TemporaryFile

models = apps.get_models()


for model in [Playlist, Song, Album, Artist, TemporaryFile]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

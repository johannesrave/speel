from django.contrib import admin
from django.apps import apps
from player.models import Playlist, Track

models = apps.get_models()


for model in [Playlist, Track]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

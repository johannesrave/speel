import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class OwnedModel(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Track(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Track")
    duration = models.IntegerField(editable=False, null=True)
    audio_file = models.FileField()

    playlist = models.ForeignKey(
        to='Playlist',
        to_field='id',
        related_name='tracks',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.title}'


class Playlist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)

    image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        quality=100,
        upload_to='images',
        max_length=1000,
        blank=True, null=True
    )

    last_track_played = models.ForeignKey(
        to='Track', to_field='id',
        blank=True, null=True,
        related_name='last_played_in_playlist',
        on_delete=models.SET_NULL)

    last_timestamp_played = models.IntegerField(
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.name}'

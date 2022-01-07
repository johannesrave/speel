import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
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


class Artist(UUIDModel):
    name = models.CharField(max_length=128, blank=True, default="Unbekannter Artist")

    def __str__(self):
        return f'{self.name}'


class Track(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Track")
    duration = models.IntegerField(editable=False, null=True)
    audio_file = models.FileField()
    artists = models.ManyToManyField(
        'Artist',
        through='TrackArtist',
        through_fields=('track', 'artist'),  # does this even work?
        related_name='tracks',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class Playlist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)

    tracks = models.ManyToManyField(
        to='Track',
        through='PlaylistTrack',
        through_fields=('playlist', 'track'),  # does this even work?
        related_name='playlists',
        blank=True,
    )
    image = ResizedImageField(
        size=[500, 500],
        crop=['middle', 'center'],
        quality=100,
        upload_to='images',
        max_length=1000,
        blank=True,
        null=True
    )
    last_track_played = models.ForeignKey(
        to='Track',
        to_field='id',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )
    last_timestamp_played = models.IntegerField(
        blank=True, null=True
    )

    def __str__(self):
        return f'{self.name}'


class Album(UUIDModel):
    title = models.CharField(max_length=128, blank=False)
    tracks = models.ManyToManyField(
        'Track',
        through='AlbumTrack',
        through_fields=('album', 'track'),
        related_name='albums',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class TemporaryFile(UUIDModel):
    file = models.FileField(upload_to='audio',
                            validators=[FileExtensionValidator(allowed_extensions=['mp3', 'webm'])])


# these explicit relation models are only there to join the M2M-models on their
# UUIDs instead of their PKIDs
# this is to enable updating the relationships by sending UUIDs via the HTTP api
# maybe it would've been easier to just use UUIDs only instead of keeping the bigint PKIDs?

class TrackArtist(UUIDModel):
    track = models.ForeignKey('Track', to_field='id', on_delete=models.CASCADE)
    artist = models.ForeignKey('Artist', to_field='id', on_delete=models.CASCADE)


class PlaylistTrack(UUIDModel):
    playlist = models.ForeignKey('Playlist', to_field='id', on_delete=models.CASCADE)
    track = models.ForeignKey('Track', to_field='id', on_delete=models.CASCADE)


class AlbumTrack(UUIDModel):
    album = models.ForeignKey('Album', to_field='id', on_delete=models.CASCADE)
    track = models.ForeignKey('Track', to_field='id', on_delete=models.CASCADE)
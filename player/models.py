import uuid
from django.db import models


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Playlist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)
    songs = models.ManyToManyField(
        'Song',
        related_name='playlists',
        blank=True,
    )

    # TODO: set default image for empty field
    thumbnail_file = models.ImageField(blank=True, null=True)
    last_song_played = models.ForeignKey(
        'Song',
        blank=True, null=True,
        on_delete=models.SET_NULL
    )


class Artist(UUIDModel):
    name = models.CharField(max_length=128, blank=True, default="Unbekannter Artist")

    def __str__(self):
        return f'{self.name}'


# TODO kann man den Titel auch aus den Meta Infos ziehen, so wie hoffentlich auch Length?
class Song(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Song")
    length = models.IntegerField(editable=False, null=True)
    audio_file = models.FileField()
    artists = models.ManyToManyField(
        'Artist',
        related_name='songs',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class Album(UUIDModel):
    title = models.CharField(max_length=128, blank=False)
    songs = models.ManyToManyField(
        'Song',
        related_name='albums',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'

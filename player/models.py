import uuid
from django.db import models


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Genre(UUIDModel):
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return f'{self.name}'


class Song(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Song")
    length = models.IntegerField(editable=False, null=True)
    artists = models.ManyToManyField('Artist', related_name='songs', blank=True, default="Unbekannter Artist")
    genre = models.ForeignKey('Genre', on_delete=models.PROTECT, default='Unbekanntes Genre')
    # album = models.ForeignKey('Album', on_delete=models.PROTECT, default='Unbekanntes Album')
    audio_file = models.FileField(blank=False)

    def __str__(self):
        return f'{self.title}'


class Album(UUIDModel):
    title = models.CharField(max_length=128, blank=False)
    artists = models.ManyToManyField('Artist', related_name='albums', blank=True, default="Unbekannter Artist")
    # artist = models.ForeignKey('Artist', on_delete=models.PROTECT, default="Unbekannter Artist")
    songs = models.ManyToManyField('Song', blank=True, related_name='songs')


class Playlist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)
    songs = models.ManyToManyField('Song', blank=True, related_name='playlists')

    def __str__(self):
        return f'{self.name}'


class Artist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return f'{self.name}'

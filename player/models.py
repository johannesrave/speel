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


class Artist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return f'{self.name}'


class Song(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Song")
    length = models.IntegerField(editable=False, null=True)
    artists = models.ManyToManyField('Artist', blank=True, null=True, related_name='songs', default=Artist.objects.get_or_create(name='Unbekannter Artist')[0])
    genre = models.ForeignKey('Genre', blank=True, null=True, on_delete=models.PROTECT, default=Genre.objects.get_or_create(name='Unbekanntes Genre')[0].pkid)
    audio_file = models.FileField()

    def __str__(self):
        return f'{self.title}'


class Album(UUIDModel):
    title = models.CharField(max_length=128, blank=False)
    artists = models.ManyToManyField('Artist', related_name='albums',  default=Artist.objects.get_or_create(name='Unbekannter Artist')[0])
    songs = models.ManyToManyField('Song', blank=True, null=True, related_name='albums', default=Song.objects.get_or_create(title='Unbekannter Song')[0].pkid)


class Playlist(UUIDModel):
    name = models.CharField(max_length=128, blank=False)
    songs = models.ManyToManyField('Song', blank=True, null=True, related_name='playlists',
                                   default=Song.objects.get_or_create(title='Unbekannter Song')[0].pkid)

    def __str__(self):
        return f'{self.name}'

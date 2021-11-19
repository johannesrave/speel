import uuid
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Genre(UUIDModel):
    name = models.CharField(max_length=128, blank=True, default="kein Genre gesetzt")

    def __str__(self):
        return f'{self.name}'


DEFAULT_GENRE_NAME = 'Ohne Genre'


def genre_default():
    return Genre.objects.get_or_create(name='DEFAULT_GENRE_NAME')[0]


class Song(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Song")
    # length = models.IntegerField(null=False, editable=False)
    length = models.IntegerField(editable=False, default=1)
    artists = models.ManyToManyField('Artist', related_name='songs', blank=True, default="Unbekannter Artist")
    # genre = models.ForeignKey('Genre',  on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.SET(genre_default))
    file = models.FileField()

    # TODO: Wenn man Gerne löscht dürfen keine Songs gelöscht werden

    def __str__(self):
        return f'{self.title}'


class Playlist(UUIDModel):
    name = models.CharField(max_length=128)
    songs = models.ManyToManyField('Song', related_name='playlists')

    def __str__(self):
        return f'{self.name}'


class Artist(UUIDModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'

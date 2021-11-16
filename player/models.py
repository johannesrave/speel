import uuid
from django.db import models


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Song(UUIDModel):
    title = models.CharField(max_length=128)
    length = models.IntegerField(null=False)
    artists = models.ManyToManyField('Artist', related_name='songs')
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    # genre = models.OneToOneField('Genre', on_delete=models.SET(self.genre_default))
    file = models.FileField()

    @staticmethod
    def genre_default():
        return Genre.objects.get_or_create(name='Ohne Genre')[0]

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


class Genre(UUIDModel):
    name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.name}'

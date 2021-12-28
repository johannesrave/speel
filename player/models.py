import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from thumbnails.fields import ImageField


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

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
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    #     default=1
    # )
    tracks = models.ManyToManyField(
        to='Track',
        through='PlaylistTrack',
        through_fields=('playlist', 'track'),  # does this even work?
        related_name='playlists',
        blank=True,
    )
    thumbnail_file = ImageField(
        upload_to='images',
        resize_source_to='large',
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

'''
# got this from https://stackoverflow.com/questions/16041232/django-delete-filefield#16041527
# it's supposed to delete files when a model is deleted or when the content of a filefield changes
# deactivating until i find the time to test it.

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.db import models


""" Whenever ANY model is deleted, if it has a file field on it, delete the associated file too"""
@receiver(post_delete)
def delete_files_when_row_deleted_from_db(sender, instance, **kwargs):
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            instance_file_field = getattr(instance, field.name)
            delete_file_if_unused(sender, instance, field, instance_file_field)


""" Delete the file if something else get uploaded in its place"""
@receiver(pre_save)
def delete_files_when_file_changed(sender, instance, **kwargs):
    # Don't run on initial save
    if not instance.pk:
        return
    for field in sender._meta.concrete_fields:
        if isinstance(field, models.FileField):
            # its got a file field. Let's see if it changed
            try:
                instance_in_db = sender.objects.get(pk=instance.pk)
            except sender.DoesNotExist:
                # We are probably in a transaction and the PK is just temporary
                # Don't worry about deleting attachments if they aren't actually saved yet.
                return
            instance_in_db_file_field = getattr(instance_in_db, field.name)
            instance_file_field = getattr(instance, field.name)
            if instance_in_db_file_field.name != instance_file_field.name:
                delete_file_if_unused(sender, instance, field, instance_in_db_file_field)


""" Only delete the file if no other instances of that model are using it"""
def delete_file_if_unused(model, instance, field, instance_file_field):
    dynamic_field = {field.name: instance_file_field.name}
    other_refs_exist = model.objects.filter(**dynamic_field).exclude(pk=instance.pk).exists()
    if not other_refs_exist:
        instance_file_field.delete(False)
'''

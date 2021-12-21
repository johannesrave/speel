import uuid
from django.db import models


class UUIDModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        abstract = True


class Artist(UUIDModel):
    name = models.CharField(max_length=128, blank=True, default="Unbekannter Artist")

    def __str__(self):
        return f'{self.name}'


# TODO kann man den Titel auch aus den Meta Infos ziehen, so wie hoffentlich auch Length?
class Song(UUIDModel):
    title = models.CharField(max_length=128, blank=True, default="Unbekannter Song")
    duration = models.IntegerField(editable=False, null=True)
    audio_file = models.FileField()
    artists = models.ManyToManyField(
        'Artist',
        related_name='songs',
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
    songs = models.ManyToManyField(
        to=Song,
        related_name='playlists',
        blank=True,
    )

    # TODO: set default image for empty field
    thumbnail_file = models.ImageField(blank=True, null=True)
    last_song_played = models.ForeignKey(
        to=Song,
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f'{self.name}'


class Album(UUIDModel):
    title = models.CharField(max_length=128, blank=False)
    songs = models.ManyToManyField(
        'Song',
        related_name='albums',
        blank=True,
    )

    def __str__(self):
        return f'{self.title}'


class TemporaryFile(UUIDModel):
    file = models.FileField()


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

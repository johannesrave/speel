#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db.models import ProtectedError
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from . import models
from .models import Genre


@receiver(pre_delete, sender=Genre, dispatch_uid='post_pre_delete_signal')
def protect_posts(sender, instance, using, **kwargs):
    if instance.name is not models.DEFAULT_GENRE_NAME:
        pass
    else:  # Any other status types I add later will also be protected
        raise ProtectedError('Only unpublished posts can be deleted.')

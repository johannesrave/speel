#!/usr/bin/python
# -*- encoding: utf-8 -*-
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from player.models import Owner


def owner_profile(sender, instance, created, **kwargs):
    if created:
        Owner.objects.create(
            user=instance,
            username=instance.username,
        )
        print('Profile created!')


post_save.connect(owner_profile, sender=User)

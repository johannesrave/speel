# Generated by Django 3.2.9 on 2021-12-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='artists',
            field=models.ManyToManyField(blank=True, related_name='albums', to='player.Artist'),
        ),
        migrations.AlterField(
            model_name='album',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='albums', to='player.Song'),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(blank=True, related_name='playlists', to='player.Song'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artists',
            field=models.ManyToManyField(blank=True, related_name='songs', to='player.Artist'),
        ),
    ]

# Generated by Django 3.2.9 on 2021-11-16 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0002_alter_song_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='file',
            field=models.FileField(upload_to=''),
        ),
    ]

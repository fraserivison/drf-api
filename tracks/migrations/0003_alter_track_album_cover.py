# Generated by Django 4.2 on 2025-01-07 03:23

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0002_alter_track_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='album_cover',
            field=cloudinary.models.CloudinaryField(blank=True, default='../default_cover', max_length=255, verbose_name='image'),
        ),
    ]
# Generated by Django 4.2 on 2025-01-07 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0003_alter_track_album_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='track',
            name='album_cover',
            field=models.ImageField(blank=True, default='../default_cover', upload_to='images/'),
        ),
    ]
# Generated by Django 5.1.4 on 2025-01-10 16:16

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ratings', '0001_initial'),
        ('tracks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='track',
            new_name='title',
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('owner', 'title')},
        ),
    ]

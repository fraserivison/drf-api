# Generated by Django 4.2 on 2025-01-17 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='track',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracks.track'),
        ),
    ]

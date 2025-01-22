"""
Models for the profiles app.

This file contains the `Profile` model, which represents a user's profile,
including details like their DJ name, bio, and profile image. It also includes
a signal to automatically create a profile when a new user is created.
"""

from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    """
    Represents a user's profile.

    This model contains information about the user, such as their DJ name,
    biography, and profile image. A `Profile` is automatically created when
    a new `User` is registered.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    dj_name = models.CharField(max_length=255, blank=True, verbose_name="DJ Name")
    bio = models.TextField(blank=True, verbose_name="About Me")
    image = models.ImageField(
        upload_to='images/',
        default='../default_profile_bp5fwp',
        blank=True
    )

    tracks = models.ManyToManyField('tracks.Track', related_name='profiles', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

def create_profile(sender, instance, created, **kwargs):
    """
    Automatically creates a profile for a user when they are registered.

    This function listens to the `post_save` signal of the `User` model and
    creates a `Profile` for the newly registered user.
    """
    if created:
        Profile.objects.create(owner=instance)

# Connect the signal
post_save.connect(create_profile, sender=User)

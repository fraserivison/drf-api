"""
This module defines the Rating model for tracking user ratings on tracks.
It also includes signal handlers to update the average track rating when
ratings are created or deleted.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from tracks.models import Track

class Rating(models.Model):
    """
    Model to represent a rating given by a user to a track.

    Fields:
    - owner: The user who gave the rating.
    - title: The track being rated.
    - created_at: Timestamp when the rating was created.
    - rating: The rating value (from 1 to 5) given by the user.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Track, related_name='ratings', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'title']

    def __str__(self):
        return f'{self.owner} rated {self.title} {self.rating}'

@receiver(post_save, sender=Rating)
def update_track_average_rating(sender, instance, created, **kwargs):
    """
    Signal handler to update the track's average rating when a new rating is created.

    Args:
        sender: The model class that triggered the signal.
        instance: The actual instance being saved.
        created: Boolean flag indicating if the instance was created.
        kwargs: Additional keyword arguments passed by the signal.
    """
    track = instance.title
    track.update_average_rating()

@receiver(post_delete, sender=Rating)
def update_track_average_rating_on_delete(sender, instance, **kwargs):
    """
    Signal handler to update the track's average rating when a rating is deleted.

    Args:
        sender: The model class that triggered the signal.
        instance: The actual instance being deleted.
        kwargs: Additional keyword arguments passed by the signal.
    """
    track = instance.title
    track.update_average_rating()

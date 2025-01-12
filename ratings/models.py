from django.db import models
from django.contrib.auth.models import User
from tracks.models import Track
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Rating(models.Model):
    """
    Rating model for rating tracks.
    'owner' is the user who is rating, 'title' is the track's title being rated.
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
    track = instance.title
    track.update_average_rating()

@receiver(post_delete, sender=Rating)
def update_track_average_rating_on_delete(sender, instance, **kwargs):
    track = instance.title
    track.update_average_rating()




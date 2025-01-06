from django.db import models
from django.contrib.auth.models import User
from tracks.models import Track

class Rating(models.Model):
    """
    Rating model for rating tracks.
    'owner' is the user who is rating, 'track' is the track being rated.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, related_name='ratings', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],  # Ratings from 1 to 5
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'track']

    def __str__(self):
        return f'{self.owner} rated {self.track} {self.rating}'


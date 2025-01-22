"""
Models for the followers app.

This file defines the Follower model, which represents the
relationship between users where one follows another.
"""

from django.db import models
from django.contrib.auth.models import User

class Follower(models.Model):
    """
    Follower model for the relationship between users:
    'owner' is the user who is following, 'followed' is the user being followed.

    The 'UniqueConstraint' ensures that duplicate follow relationships are not allowed.
    """
    owner = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followed', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['owner', 'followed'], name='unique_follow')
        ]

    def __str__(self):
        return f'{self.owner} follows {self.followed}'

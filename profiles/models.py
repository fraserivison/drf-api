from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
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
        return f"{self.username}'s profile"

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(username=instance)

post_save.connect(create_profile, sender=User)





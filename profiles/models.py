from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True, verbose_name="DJ Name")
    bio = models.TextField(blank=True, verbose_name="About Me")
    image = models.ImageField(
        upload_to='images/',
        default='../default_profile_bp5fwp',
        blank=True
    )

    # Reference to the Track model in the 'tracks' app (if this is where it's defined)
    tracks = models.ManyToManyField('tracks.Track', related_name='profiles', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"

def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)

post_save.connect(create_profile, sender=User)




from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Avg
from profiles.models import Profile

local_storage = FileSystemStorage(location=settings.MEDIA_ROOT)

class Track(models.Model):
    GENRE_CHOICES = [
        ('house', 'House'),
        ('tech_house', 'Tech House'),
        ('trance', 'Trance'),
        ('dubstep', 'Dubstep'),
        ('drum_and_bass', 'Drum and Bass'),
        ('techno', 'Techno'),
        ('electro', 'Electro'),
        ('progressive_house', 'Progressive House'),
        ('chillout', 'Chillout'),
        ('other', 'Other'),
    ]

    username = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="user_tracks", null=True
    )  # Allow null temporarily
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    audio_file = models.FileField(upload_to='audio_files/', storage=local_storage)
    album_cover = models.ImageField(
        upload_to='album_covers/',
        storage=local_storage,
        default='../default_cover',
        blank=True
    )
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ratings_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'

    def update_average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        self.average_rating = avg_rating if avg_rating else 0
        self.ratings_count = self.ratings.count()
        self.save()



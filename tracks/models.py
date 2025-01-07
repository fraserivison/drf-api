from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    """
    Track model for sharing music.
    """
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

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='other')
    audio_file = models.FileField(upload_to='audio_files/')
    album_cover = models.ImageField(
        upload_to='album_covers/',
        default='../default_album_cover',
        blank=True
    )
    
    # Ratings-related fields
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    ratings_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'

    def update_average_rating(self):
        total_rating = sum(rating.value for rating in self.ratings.all())
        total_ratings = self.ratings.count()
        if total_ratings > 0:
            self.average_rating = total_rating / total_ratings
        else:
            self.average_rating = 0.00
        self.ratings_count = total_ratings
        self.save()




from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """
    Event model to allow users to advertise events.
    Includes details like name, date, location, genre, etc.
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
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    genre = models.CharField(
        max_length=50,
        choices=GENRE_CHOICES,
        blank=False,
        null=False
    )
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name



from rest_framework import serializers
from .models import Track
from profiles.serializers import ProfileSerializer

class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile = ProfileSerializer(source='owner.profile', read_only=True)
    average_rating = serializers.ReadOnlyField(source='average_rating_annotation')
    ratings_count = serializers.ReadOnlyField(source='ratings_count_annotation')
    
    # Ensure album_cover is only returned as the Cloudinary image URL
    album_cover = serializers.CharField(source='album_cover.url', read_only=True)

    class Meta:
        model = Track
        fields = [
            'id', 'owner', 'profile', 'created_at', 'updated_at', 'title', 
            'description', 'genre', 'audio_file', 'album_cover',  # album_cover will show Cloudinary URL
            'average_rating', 'ratings_count',
        ]
        read_only_fields = ['album_cover', 'average_rating', 'ratings_count']


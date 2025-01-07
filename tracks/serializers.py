from rest_framework import serializers
from .models import Track
from profiles.serializers import ProfileSerializer

class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile = ProfileSerializer(source='owner.profile', read_only=True)
    average_rating = serializers.ReadOnlyField(source='average_rating_annotation')
    ratings_count = serializers.ReadOnlyField(source='ratings_count_annotation')

    def validate_audio_file(self, value):
        if value.size > 100 * 1024 * 1024:  # Increased to 100MB limit
            raise serializers.ValidationError('Audio file size larger than 100MB!')
        if not value.name.endswith(('.mp3', '.wav', '.flac')):
            raise serializers.ValidationError('Invalid audio file format!')
        return value

    def validate_album_cover(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit for album cover
            raise serializers.ValidationError('Image size larger than 5MB!')
        if value.image.height > 4096 or value.image.width > 4096:
            raise serializers.ValidationError('Image dimensions larger than 4096px!')
        return value

    class Meta:
        model = Track
        fields = [
            'id', 'owner', 'profile', 'created_at', 'updated_at', 'title', 
            'description', 'genre', 'audio_file', 'album_cover',
            'average_rating', 'ratings_count',
        ]

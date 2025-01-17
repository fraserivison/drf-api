from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.owner')
    average_rating = serializers.ReadOnlyField(source='average_rating_annotation')
    ratings_count = serializers.ReadOnlyField(source='ratings_count_annotation')

    def validate_audio_file(self, value):
        if value.size > 100 * 1024 * 1024:
            raise serializers.ValidationError('Audio file size larger than 100MB!')
        if not value.name.endswith(('.mp3', '.wav', '.flac')):
            raise serializers.ValidationError('Invalid audio file format!')
        return value

    class Meta:
        model = Track
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 
            'description', 'genre', 'audio_file', 'album_cover',
            'average_rating', 'ratings_count',
        ]

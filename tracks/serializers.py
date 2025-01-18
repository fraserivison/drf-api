from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.ReadOnlyField()
    ratings_count = serializers.ReadOnlyField()

    def validate_audio_file(self, value):
        if value is None:
            return value
        
        if value.size > 100 * 1024 * 1024:
            raise serializers.ValidationError('Audio file size larger than 100MB!')
        if not value.name.endswith(('.mp3', '.wav', '.flac')):
            raise serializers.ValidationError('Invalid audio file format!')
        return value

    def update(self, instance, validated_data):
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

    class Meta:
        model = Track
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 
            'description', 'genre', 'audio_file', 'album_cover',
            'average_rating', 'ratings_count',
        ]
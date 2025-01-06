from rest_framework import serializers
from .models import Track


class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_audio_file(self, value):
        if value.size > 10 * 1024 * 1024:  # 10MB limit
            raise serializers.ValidationError('Audio file size larger than 10MB!')
        if not value.name.endswith(('.mp3', '.wav', '.flac')):
            raise serializers.ValidationError('Invalid audio file format!')
        return value

    def validate_album_cover(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB limit
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.height > 4096 or value.image.width > 4096:
            raise serializers.ValidationError('Image dimensions larger than 4096px!')
        return value

    class Meta:
        model = Track
        fields = [
            'id', 'owner', 'profile_id', 'profile_image', 
            'created_at', 'updated_at', 'title', 
            'description', 'genre', 'audio_file', 'album_cover',
        ]
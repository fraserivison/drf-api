from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    """
    Serializer for the Track model, including fields for rating and audio file.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.ReadOnlyField()
    ratings_count = serializers.ReadOnlyField()
    audio_file_url = serializers.SerializerMethodField()

    def validate_audio_file(self, value):
        """
        Validate the audio file to ensure it's within size limits and has the correct format.
        """
        if value is None:
            return value
        if value.size > 100 * 1024 * 1024:
            raise serializers.ValidationError('Audio file size larger than 100MB!')
        if not value.name.endswith(('.mp3', '.wav', '.flac')):
            raise serializers.ValidationError('Invalid audio file format!')
        return value

    def get_audio_file_url(self, obj):
        """
        Get the URL for the audio file if it exists.
        """
        if obj.audio_file:
            return obj.audio_file.url
        return None

    def update(self, instance, validated_data):
        """
        Update the track instance with validated data and save it.
        """
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.save()
        return instance

    class Meta:
        model = Track
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'title', 
            'description', 'genre', 'audio_file', 'album_cover',
            'average_rating', 'ratings_count', 'audio_file_url',
        ]

from rest_framework import serializers
from .models import Track

class TrackSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    average_rating = serializers.ReadOnlyField()
    ratings_count = serializers.ReadOnlyField()
    audio_file_url = serializers.SerializerMethodField()

    def validate_audio_file(self, value):
        if value is None:
            return value

        # Check if value is a Cloudinary resource (you might need to adjust depending on your configuration)
        if hasattr(value, 'file'):
            # This checks for the file size when using Cloudinary
            file_size = value.file.size  # Accessing the file's size
        else:
            file_size = value.size  # Use size directly if it's a normal file

        # Validate file size
        if file_size > 100 * 1024 * 1024:
            raise serializers.ValidationError('Audio file size larger than 100MB!')
        
        # Validate file format
        if not value.name.endswith(('.mp3', '.wav', '.flac')):
            raise serializers.ValidationError('Invalid audio file format!')
        
        return value

    def get_audio_file_url(self, obj):
        if obj.audio_file:
            return obj.audio_file.url
        return None

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
            'average_rating', 'ratings_count', 'audio_file_url',
        ]

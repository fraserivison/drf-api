from django.db import IntegrityError
from rest_framework import serializers
from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model
    The create method handles updating an existing rating if it already exists.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'owner', 'track', 'rating']

    def create(self, validated_data):
        # Check if the user has already rated the track
        user = validated_data.get('owner')
        track = validated_data.get('track')

        existing_rating = Rating.objects.filter(owner=user, track=track).first()

        if existing_rating:
            # If a rating already exists, update it instead of creating a new one
            existing_rating.rating = validated_data['rating']
            existing_rating.save()
            return existing_rating
        else:
            return super().create(validated_data)


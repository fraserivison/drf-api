from rest_framework import serializers
from .models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model. Ensures that a user can only rate a track once.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'owner', 'title', 'rating']

    def create(self, validated_data):
        """
        Ensure that each user can only create or update one rating per track.
        If a rating exists, update it; otherwise, create a new one.
        """
        existing_rating = Rating.objects.filter(owner=validated_data['owner'], title=validated_data['title']).first()

        if existing_rating:
            existing_rating.rating = validated_data['rating']
            existing_rating.save()
            return existing_rating
        else:
            return Rating.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Ensure we only update the rating value, and no other fields.
        """
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

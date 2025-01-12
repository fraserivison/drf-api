from rest_framework import serializers
from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Simplified Serializer for the Rating model.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'owner', 'title', 'rating']

    def create(self, validated_data):
        """
        Ensure that each user can only create one rating per track.
        If a rating exists, return it; otherwise, create a new one.
        """
        rating, created = Rating.objects.update_or_create(
            owner=validated_data['owner'],
            title=validated_data['title'],
            defaults={'rating': validated_data['rating']}
        )
        return rating






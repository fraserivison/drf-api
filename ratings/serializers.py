from rest_framework import serializers
from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Simplified Serializer for the Rating model.
    """
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'username', 'title', 'rating']

    def create(self, validated_data):
        """
        Ensure that each user can only create one rating per track.
        If a rating exists, return it; otherwise, create a new one.
        """
        rating, created = Rating.objects.update_or_create(
            username=validated_data['username'],
            title=validated_data['title'],
            defaults={'rating': validated_data['rating']}
        )
        return rating






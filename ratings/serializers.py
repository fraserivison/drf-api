from django.db import IntegrityError
from rest_framework import serializers
from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model
    The create method handles the unique constraint on 'owner' and 'track'
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'owner', 'track', 'rating']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': 'You have already rated this track.'
            })

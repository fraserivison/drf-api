"""
Serializers for the followers app.

This file contains serializers for managing follow relationships between users.
It includes validation to prevent following oneself or duplicating follow relationships.
"""

from rest_framework import serializers
from django.db.utils import IntegrityError
from .models import Follower

class FollowerSerializer(serializers.ModelSerializer):
    """
    Serializer to manage follower data and user relationships.

    Adjusted to use read-only fields and handle duplicate follow attempts.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    followed_owner = serializers.ReadOnlyField(source='followed.profile.owner.username')
    followed_profile_id = serializers.ReadOnlyField(source='followed.profile.id')
    followed_profile_image = serializers.ReadOnlyField(source='followed.profile.image.url')

    class Meta:
        model = Follower
        fields = [
            'id',
            'owner',
            'created_at',
            'followed',
            'followed_owner',
            'followed_profile_id',
            'followed_profile_image',
        ]

    def create(self, validated_data):
        """
        Handle the creation of a new follow relationship.
        
        Validates that a user cannot follow themselves and ensures the follow 
        relationship is unique. Raises validation errors if these conditions are violated.
        """
        owner = validated_data.get('owner')
        followed = validated_data.get('followed')
        if owner == followed:
            raise serializers.ValidationError({'detail': 'You cannot follow yourself.'})
        if Follower.objects.filter(owner=owner, followed=followed).exists():
            raise serializers.ValidationError({'detail': 'This user is already followed.'})
        return super().create(validated_data)

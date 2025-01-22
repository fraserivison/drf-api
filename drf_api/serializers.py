"""
This module defines serializers for user-related data, including the current user.
"""

from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    """
    Serializer for the current user, extending the UserDetailsSerializer
    to include profile-related information (ID and image).
    """
    profile_id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')

    class Meta(UserDetailsSerializer.Meta):
        """
        Meta class to define additional fields to include in the serialized data.
        """
        fields = UserDetailsSerializer.Meta.fields + (
            'profile_id', 'profile_image'
        )

    # pylint: disable=too-few-public-methods

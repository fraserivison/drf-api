"""
Serializers for the profiles app.

This file contains the `ProfileSerializer`, which is responsible for serializing
profile data and related information such as tracks, events, and follow relationships.
It provides additional fields to manage the user's following status, event participation,
and track ownership.
"""

from rest_framework import serializers
from followers.models import Follower
from events.models import Event
from events.serializers import EventSerializer
from tracks.models import Track
from tracks.serializers import TrackSerializer
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer to manage profile data and related information.

    This serializer provides the following fields:
    - Profile details (owner, DJ name, bio, image, etc.)
    - Whether the current user is the owner of the profile
    - The ID of the currently following user (if authenticated)
    - Counts for followers and following
    - Events associated with the profile owner
    - Tracks associated with the profile owner
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    events = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Checks if the current user is the owner of the profile.

        Returns a boolean indicating whether the profile belongs to the current user.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        """
        Retrieves the ID of the follow relationship between the current user and the profile owner.

        If the current user is not following the profile owner, returns None.
        """
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_events(self, obj):
        """
        Retrieves the events associated with the profile owner.

        Returns a serialized list of events that belong to the profile owner.
        """
        events = Event.objects.filter(owner=obj.owner)
        return EventSerializer(events, many=True).data

    def get_tracks(self, obj):
        """
        Retrieves the tracks associated with the profile owner.

        Returns a serialized list of tracks that belong to the profile owner.
        """
        tracks = Track.objects.filter(owner=obj.owner)
        return TrackSerializer(tracks, many=True).data

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'dj_name',
            'bio', 'image', 'is_owner', 'following_id', 'followers_count', 
            'following_count', 'events', 'tracks'
        ]

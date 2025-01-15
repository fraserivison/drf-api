from rest_framework import serializers
from .models import Profile
from followers.models import Follower
from events.models import Event
from events.serializers import EventSerializer
from tracks.models import Track


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    events = serializers.SerializerMethodField()
    tracks = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_following_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = Follower.objects.filter(
                owner=user, followed=obj.owner
            ).first()
            return following.id if following else None
        return None

    def get_events(self, obj):
        events = Event.objects.filter(owner=obj.owner)
        return EventSerializer(events, many=True).data

    def get_tracks(self, obj):
        from tracks.serializers import TrackSerializer
        tracks = Track.objects.filter(owner=obj.owner)
        return TrackSerializer(tracks, many=True).data

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'dj_name',
            'bio', 'image', 'is_owner', 'following_id', 'followers_count', 
            'following_count', 'events', 'tracks'
        ]

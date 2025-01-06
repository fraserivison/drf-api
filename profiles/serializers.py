from rest_framework import serializers
from .models import Profile
from followers.models import Follower


class ProfileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    following_id = serializers.SerializerMethodField()
    track_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

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

    def get_track_count(self, obj):
        return obj.track_set.count()  # Assuming Profile is linked to tracks

    def get_followers_count(self, obj):
        return Follower.objects.filter(followed=obj.owner).count()

    def get_following_count(self, obj):
        return Follower.objects.filter(owner=obj.owner).count()

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at', 'updated_at', 'dj_name',
            'bio', 'image', 'is_owner', 'following_id',
            'track_count', 'followers_count', 'following_count',
        ]

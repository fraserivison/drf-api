from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    Includes fields for the user's profile and formatted timestamps.
    """
    username = serializers.ReadOnlyField(source='username.username')
    is_username = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='username.profile.id')
    profile_image = serializers.ReadOnlyField(source='username.profile.image.url')
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_is_username(self, obj):
        request = self.context['request']
        return request.user == obj.username

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    class Meta:
        model = Comment
        fields = [
            'id', 'username', 'is_username', 'profile_id', 'profile_image',
            'track', 'created_at', 'updated_at', 'content'
        ]


class CommentDetailSerializer(CommentSerializer):
    """
    Serializer for the Comment model used in the Detail view.
    Track is read-only so it's automatically assigned on creation.
    """
    track = serializers.ReadOnlyField(source='track.id')

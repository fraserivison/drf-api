"""
Views for the followers app.

This file contains views to manage follower relationships,
such as listing followers, following users, and unfollowing users.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from drf_api.permissions import IsownerOrReadOnly
from .serializers import FollowerSerializer
from .models import Follower

class FollowerList(generics.ListCreateAPIView):
    """
    View to list all followers and allow users to follow others.

    Adjusted for profile integration and user relationships.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    View to retrieve details of a follower and allow unfollowing.
    """
    permission_classes = [IsownerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_destroy(self, instance):
        target_user = instance.followed
        follow_instance = Follower.objects.filter(owner=self.request.user,
        followed=target_user).first()

        if not follow_instance:
            return Response({"detail": "You are not following this user."},
            status=status.HTTP_400_BAD_REQUEST)

        follow_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

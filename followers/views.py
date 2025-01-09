from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from .models import Follower
from .serializers import FollowerSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework import status

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


class FollowerDetail(generics.RetrieveDestroyAPIView):  # Change here
    """
    View to retrieve details of a follower and allow unfollowing.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_destroy(self, instance):
        # Get the user trying to unfollow
        target_user = instance.followed

        # Check if the current user is following the target user
        follow_instance = Follower.objects.filter(owner=self.request.user, followed=target_user).first()

        if not follow_instance:
            raise ValidationError("You are not following this user.")  # Raise error if not following

        # Delete the relationship
        follow_instance.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)  # Return successful response






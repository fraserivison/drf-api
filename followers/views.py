from rest_framework.exceptions import ValidationError
from rest_framework import generics, permissions
from .models import Follower
from .serializers import FollowerSerializer
from drf_api.permissions import IsusernameOrReadOnly
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
        serializer.save(username=self.request.user)


class FollowerDetail(generics.RetrieveDestroyAPIView):
    """
    View to retrieve details of a follower and allow unfollowing.
    """
    permission_classes = [IsusernameOrReadOnly]
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

    def perform_destroy(self, instance):
        target_user = instance.followed
        follow_instance = Follower.objects.filter(username=self.request.user, followed=target_user).first()

        if not follow_instance:
            raise ValidationError("You are not following this user.")
        follow_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)






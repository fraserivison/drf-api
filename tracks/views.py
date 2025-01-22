from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from profiles.models import Profile
from .models import Track
from .serializers import TrackSerializer
from drf_api.permissions import IsownerOrReadOnly

class TrackList(generics.ListCreateAPIView):
    """
    API view to list all tracks or create a new track.
    """
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Track.objects.annotate(
        ratings_count_annotation=Count('ratings', distinct=True),
        average_rating_annotation=Avg('ratings__rating')
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['owner', 'genre']
    search_fields = ['owner__username', 'title', 'description', 'genre']
    ordering_fields = ['ratings_count_annotation', 'created_at']

    def perform_create(self, serializer):
        """
        Create a new track, linking it to the user's profile.
        """
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(owner=user)
        serializer.save(owner=user, profile=profile)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update or delete a track.
    """
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Track.objects.annotate(
        ratings_count_annotation=Count('ratings', distinct=True),
        average_rating_annotation=Avg('ratings__rating')
    )

    def perform_update(self, serializer):
        """
        Update the track, keeping the owner as the current user.
        """
        serializer.save(owner=self.request.user, partial=True)

    def perform_destroy(self, instance):
        """
        Delete the track.
        """
        instance.delete()

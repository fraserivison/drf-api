from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from profiles.models import Profile
from .models import Track
from .serializers import TrackSerializer

class TrackList(generics.ListCreateAPIView):
    """
    List tracks or create a track if logged in.
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
    filterset_fields = ['owner', 'genre']  # Adjusted to directly filter by owner
    search_fields = ['owner__username', 'title', 'description', 'genre']
    ordering_fields = ['ratings_count_annotation', 'created_at']

    def perform_create(self, serializer):
        user = self.request.user
        # Ensure the profile is created for the user if it doesn't exist
        profile, created = Profile.objects.get_or_create(owner=user)
        # Save the track with the profile as the owner
        serializer.save(owner=profile)

class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a track and edit or delete it if you own it.
    """
    serializer_class = TrackSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Track.objects.annotate(
        ratings_count_annotation=Count('ratings', distinct=True),
        average_rating_annotation=Avg('ratings__rating')
    ).order_by('-created_at')

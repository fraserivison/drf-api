from django.db.models import Count
from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_api.permissions import IsOwnerOrReadOnly
from .models import Track
from .serializers import TrackSerializer

class TrackList(generics.ListCreateAPIView):
    """
    List tracks or create a track if logged in.
    """
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Track.objects.annotate(
        ratings_count=Count('ratings', distinct=True),
        average_rating=models.Avg('ratings__value')
    ).order_by('-created_at')
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_fields = ['owner__profile', 'genre']
    search_fields = ['owner__username', 'title', 'description', 'genre']
    ordering_fields = ['ratings_count', 'created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a track and edit or delete it if you own it.
    """
    serializer_class = TrackSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Track.objects.annotate(
        ratings_count=Count('ratings', distinct=True),
        average_rating=models.Avg('ratings__value')
    ).order_by('-created_at')

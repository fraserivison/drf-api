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
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')
    
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    
    # Fields to filter by in the URL (e.g., /tracks/?owner__profile=<profile_id>)
    filterset_fields = ['owner__profile', 'genre']
    
    # Fields to search by in the URL (e.g., /tracks/?search=<search_term>)
    search_fields = ['owner__username', 'title', 'description', 'genre']
    
    # Fields to order by in the URL (e.g., /tracks/?ordering=likes_count)
    ordering_fields = ['likes_count', 'created_at']

    def perform_create(self, serializer):
        """
        Set the owner of the track to the current authenticated user when creating a track.
        """
        serializer.save(owner=self.request.user)


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a track and edit or delete it if you own it.
    """
    serializer_class = TrackSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
    queryset = Track.objects.annotate(
        likes_count=Count('likes', distinct=True)
    ).order_by('-created_at')

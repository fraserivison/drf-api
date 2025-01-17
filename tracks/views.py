from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Avg
from .models import Track
from .serializers import TrackSerializer
from profiles.models import Profile
from drf_api.permissions import IsownerOrReadOnly


class TrackList(generics.ListCreateAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]
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
    search_fields = ['owner__owner', 'title', 'description', 'genre']
    ordering_fields = ['ratings_count_annotation', 'created_at']

    def perform_create(self, serializer):
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(owner=user)
        serializer.save(owner=user, profile=profile)  


class TrackDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated, IsownerOrReadOnly]
    queryset = Track.objects.annotate(
        ratings_count_annotation=Count('ratings', distinct=True),
        average_rating_annotation=Avg('ratings__rating')
    )
    
    def perform_destroy(self, instance):
        instance.delete()


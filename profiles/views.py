from django.db.models import Count
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer

class ProfileList(generics.ListAPIView):
    """
    List all profiles with track count, followers count, and following count.
    """
    queryset = Profile.objects.annotate(
        track_count=Count('tracks', distinct=True),  # Correct relationship to Track model
        followers_count=Count('owner__followed', distinct=True),  # Correct reverse relationship
        following_count=Count('owner__following', distinct=True)  # Correct reverse relationship
    ).order_by('-created_at')

    serializer_class = ProfileSerializer

    filter_backends = [
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    
    filterset_fields = [
        'owner__following__followed__profile',
        'owner__followed__owner__profile',
    ]
    
    ordering_fields = [
        'track_count',
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    queryset = Profile.objects.annotate(
        track_count=Count('tracks', distinct=True),  # Correct relationship to Track model
        followers_count=Count('owner__followed', distinct=True),  # Correct reverse relationship
        following_count=Count('owner__following', distinct=True)  # Correct reverse relationship
    ).order_by('-created_at')

    serializer_class = ProfileSerializer



from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsownerOrReadOnly
from dj_rest_auth.views import LoginView
from rest_framework.response import Response

class ProfileList(generics.ListAPIView):
    """
    List all profiles with followers count and following count.
    """
    queryset = Profile.objects.all()
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
        'followers_count',
        'following_count',
        'owner__following__created_at',
        'owner__followed__created_at',
    ]

    permission_classes = [IsownerOrReadOnly]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsownerOrReadOnly]

class CustomLoginView(LoginView):
    def get_response(self):
        response = super().get_response()

        user = self.user
        
        profile = user.profile 
        
        response.data['profile_id'] = profile.id
        return response  

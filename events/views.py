from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class EventList(generics.ListCreateAPIView):
    """
    List all events or create a new event.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event if the user is the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

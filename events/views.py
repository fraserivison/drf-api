from rest_framework import generics, permissions
from .models import Event
from .serializers import EventSerializer
from drf_api.permissions import IsusernameOrReadOnly

class EventList(generics.ListCreateAPIView):
    """
    List all events or create a new event.
    """
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(username=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event if the user is the username.
    """
    permission_classes = [IsusernameOrReadOnly]
    queryset = Event.objects.all()
    serializer_class = EventSerializer

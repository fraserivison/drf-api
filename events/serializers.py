from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Event
        fields = ['id', 'owner', 'name', 'description', 'genre', 'date', 'location', 'created_at', 'updated_at']

from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.username')

    class Meta:
        model = Event
        fields = [
            'id', 'username', 'name', 'description', 'genre', 'date', 'location', 'created_at', 'updated_at'
        ]
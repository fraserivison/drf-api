"""
Serializers for the events app.

This file contains the serializers used to serialize and deserialize Event model data.
"""

from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    """
    Serializer for the Event model.

    This serializer converts Event model instances into JSON format and validates 
    incoming data to ensure it can be deserialized into an Event instance.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'name', 'description', 'genre', 'date',
            'location', 'created_at', 'updated_at'
        ]

    def update(self, instance, validated_data):
        """
        Custom update method for partial updates. 
        Only the fields provided in validated_data will be updated.
        """
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        return instance

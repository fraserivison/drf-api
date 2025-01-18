from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Event
        fields = [
            'id', 'owner', 'name', 'description', 'genre', 'date', 'location', 'created_at', 'updated_at'
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

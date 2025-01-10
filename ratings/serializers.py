from rest_framework import serializers
from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model.
    The create method handles updating an existing rating if it already exists.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    title_name = serializers.SerializerMethodField()  # Use SerializerMethodField to fetch the track title

    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'owner', 'title', 'title_name', 'rating']  # Add 'title_name' to the fields

    def get_title_name(self, obj):
        # Use the 'title' field from the related Track model
        return obj.title.title if obj.title else None  # Adjusted to use the correct field name ('title')

    def create(self, validated_data):
        # Check if the user has already rated the track
        user = validated_data.get('owner')
        title = validated_data.get('title')  # Using 'title' instead of 'track'

        existing_rating = Rating.objects.filter(owner=user, title=title).first()

        if existing_rating:
            # If a rating already exists, update it instead of creating a new one
            existing_rating.rating = validated_data['rating']
            existing_rating.save()
            return existing_rating
        else:
            return super().create(validated_data)






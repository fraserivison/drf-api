from rest_framework import serializers
from ratings.models import Rating

class RatingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Rating model.
    The create method handles updating an existing rating if it already exists.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    title_name = serializers.SerializerMethodField()
    class Meta:
        model = Rating
        fields = ['id', 'created_at', 'owner', 'title', 'title_name', 'rating']

    def get_title_name(self, obj):
        return obj.title.title if obj.title else None

    def create(self, validated_data):
        user = validated_data.get('owner')
        title = validated_data.get('title')

        existing_rating = Rating.objects.filter(owner=user, title=title).first()

        if existing_rating:
            existing_rating.rating = validated_data['rating']
            existing_rating.save()
            return existing_rating
        else:
            return super().create(validated_data)






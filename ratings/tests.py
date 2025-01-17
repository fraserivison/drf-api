from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Rating
from tracks.models import Track

class RatingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(owner='testuser', password='password123')
        
        self.track = Track.objects.create(
            owner=self.user,
            title='Test Track',
            description='A test track description.',
            genre='house',
        )

        self.client = APIClient()
        self.create_url = '/ratings/'

    def test_only_logged_in_users_can_rate(self):
        """Test that only logged-in users can rate a track"""
        rating_data = {
            'track': self.track.id,
            'rating': 4
        }
        response = self.client.post(self.create_url, rating_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Rating.objects.count(), 0)


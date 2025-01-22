"""
This module contains test cases for the Rating model, ensuring that users
can rate tracks only when logged in, and that the system behaves as expected
with respect to ratings.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from tracks.models import Track
from .models import Rating

class RatingTests(APITestCase):
    """
    Test suite for the Rating model, verifying user permissions and rating logic.
    """

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create a track for testing
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



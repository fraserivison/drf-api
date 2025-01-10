from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Rating
from tracks.models import Track

class RatingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.track = Track.objects.create(
            owner=self.user.profile,
            title='Test Track',
            description='A test track description.',
            genre='house',
        )
        self.client = APIClient()
        self.create_url = '/ratings/'

    def test_logged_in_user_can_rate_track(self):
        self.client.login(username='testuser', password='password123')

        rating_data = {
            'title': self.track.id,
            'rating': 4
        }

        response = self.client.post(self.create_url, rating_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().rating, 4)

        
    def test_user_can_update_rating(self):
        """
        Test that a user can update their rating for a track by submitting a new rating.
        """
        self.client.login(username='testuser', password='password123')

        initial_rating_data = {
            'title': self.track.id,
            'rating': 3
        }
        response = self.client.post(self.create_url, initial_rating_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().rating, 3)

        updated_rating_data = {
            'title': self.track.id,
            'rating': 5
        }
        response = self.client.post(self.create_url, updated_rating_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().rating, 5)

    def test_only_logged_in_users_can_rate(self):
        rating_data = {
            'title': self.track.id,
            'rating': 4
        }
        response = self.client.post(self.create_url, rating_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Rating.objects.count(), 0)

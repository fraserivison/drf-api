from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Follower
from rest_framework.exceptions import ValidationError


class FollowerTests(APITestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        # Log in as user1
        self.client.login(username='user1', password='testpass')
        # Clear all existing Follower objects
        Follower.objects.all().delete()

    def test_follow_user(self):
        """
        Test that a user can follow another user.
        """
        # Perform POST request to follow user2
        response = self.client.post('/followers/', {'followed': self.user2.id})
        # Check response status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify Follower object exists in the database
        self.assertTrue(Follower.objects.filter(owner=self.user1, followed=self.user2).exists())

        from rest_framework.exceptions import ValidationError

    
    def test_duplicate_follow(self):
        """
        Test that a user cannot follow the same user twice.
        """
        # Follow the user once
        response1 = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Attempt to follow the same user again
        response2 = self.client.post('/followers/', {'followed': self.user2.id})
    
        # Check that the response is a 400 Bad Request due to duplicate follow
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This user is already followed.', str(response2.data))

        # Ensure that the follow relationship only exists once in the database
        self.assertEqual(Follower.objects.filter(owner=self.user1, followed=self.user2).count(), 1)

    def test_unfollow_user(self):
        """
        Test that a user can unfollow another user.
        """
        # First, follow user2
        response1 = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Get the follower relationship ID
        follower_id = Follower.objects.get(owner=self.user1, followed=self.user2).id

        # Now unfollow user2
        response2 = self.client.delete(f'/followers/{follower_id}/')
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)

        # Ensure that the follow relationship is removed
        self.assertFalse(Follower.objects.filter(owner=self.user1, followed=self.user2).exists())


    def test_retrieve_follower_detail(self):
        """
        Test that a user can retrieve details of a specific follower relationship.
        """
        # Create a follow relationship
        follow = Follower.objects.create(owner=self.user1, followed=self.user2)

        # Perform GET request for the specific follower detail
        response = self.client.get(f'/followers/{follow.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify the response contains the correct follower details
        self.assertEqual(response.data['owner'], self.user1.username)  # Updated to check the username
        self.assertEqual(response.data['followed'], self.user2.id)


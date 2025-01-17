from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Follower


class FollowerTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='testpass')
        self.user2 = User.objects.create_user(username='user2', password='testpass')
        self.client.login(username='user1', password='testpass')
        Follower.objects.all().delete()

    def test_follow_user(self):
        """
        Test that a user can follow another user.
        """
        response = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follower.objects.filter(username=self.user1, followed=self.user2).exists())

    def test_duplicate_follow(self):
        """
        Test that a user cannot follow the same user twice.
        """
        response1 = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        response2 = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('This user is already followed.', str(response2.data))

        self.assertEqual(Follower.objects.filter(username=self.user1, followed=self.user2).count(), 1)

    def test_unfollow_user(self):
        """
        Test that a user can unfollow another user.
        """
        response1 = self.client.post('/followers/', {'followed': self.user2.id})
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        follower_id = Follower.objects.get(username=self.user1, followed=self.user2).id

        response2 = self.client.delete(f'/followers/{follower_id}/')
        self.assertEqual(response2.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Follower.objects.filter(username=self.user1, followed=self.user2).exists())

    def test_retrieve_follower_detail(self):
        """
        Test that a user can retrieve details of a specific follower relationship.
        """
        follow = Follower.objects.create(username=self.user1, followed=self.user2)

        response = self.client.get(f'/followers/{follow.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['username'], self.user1.username)
        self.assertEqual(response.data['followed'], self.user2.id)

    def test_follow_self(self):
        """
        Test that a user cannot follow themselves.
        """
        response = self.client.post('/followers/', {'followed': self.user1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You cannot follow yourself.', str(response.data))

        self.assertFalse(Follower.objects.filter(username=self.user1, followed=self.user1).exists())



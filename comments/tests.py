from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Comment
from tracks.models import Track
import json

class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.track = Track.objects.create(
            owner=self.user,
            title='Test Track',
            genre='house',
            audio_file='test_audio.mp3',
        )

        self.comment = Comment.objects.create(
            owner=self.user,
            track=self.track,
            content="This is a test comment."
        )

    def test_post_comment(self):
        """
        Test that a logged-in user can post a comment on a track.
        """
        response = self.client.post('/comments/', {'track': self.track.id, 'content': 'New comment'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_edit_own_comment(self):
        """
        Test that a logged-in user can edit their own comment
        and cannot edit someone else's comment.
        """
        comment = Comment.objects.create(
            owner=self.user, track=self.track, content="Original Comment"
        )

        response = self.client.put(
            f'/comments/{comment.id}/',
            json.dumps({'content': 'Updated Comment'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated Comment')

        new_user = User.objects.create_user(username='otheruser', password='testpass')
        other_comment = Comment.objects.create(
            owner=new_user, track=self.track, content="Other User Comment"
        )

        response = self.client.put(
            f'/comments/{other_comment.id}/',
            json.dumps({'content': 'Hacked Comment'}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_own_comment(self):
        """
        Test that a logged-in user can delete their own comment
        """
        response = self.client.delete(f'/comments/{self.comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())


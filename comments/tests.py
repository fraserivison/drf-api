from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from comments.models import Comment
from tracks.models import Track
import json

class CommentTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Create a track
        self.track = Track.objects.create(
            owner=self.user.profile,
            title='Test Track',
            genre='house',
            audio_file='test_audio.mp3',
        )

        # Create a comment
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
        # Create a comment by the logged-in user
        comment = Comment.objects.create(
            owner=self.user, track=self.track, content="Original Comment"
        )

        # Attempt to edit the comment (success case)
        response = self.client.put(
            f'/comments/{comment.id}/',
            json.dumps({'content': 'Updated Comment'}),  # Use json.dumps for payload
            content_type='application/json'
        )
        print(response.data)  # Debug: Log response data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Updated Comment')

        # Create a new user and comment for failure case
        new_user = User.objects.create_user(username='otheruser', password='testpass')
        other_comment = Comment.objects.create(
            owner=new_user, track=self.track, content="Other User Comment"
        )

        # Attempt to edit someone else's comment (failure case)
        response = self.client.put(
            f'/comments/{other_comment.id}/',
            json.dumps({'content': 'Hacked Comment'}),  # Use json.dumps for payload
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

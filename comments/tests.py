from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from comments.models import Comment
from tracks.models import Track

class CommentTests(APITestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Create a track
        self.track = Track.objects.create(
            owner=self.user.profile,  # Ensure you are using the profile
            title='Test Track',
            genre='house',
            audio_file='test_audio.mp3',  # Ensure this is valid or mocked
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

    # Add more tests here as needed


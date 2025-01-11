from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Track
from django.core.files.uploadedfile import SimpleUploadedFile


class TrackTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.profile, created = Profile.objects.get_or_create(owner=self.user)
        self.client.login(username='testuser', password='password123')


    def test_create_track(self):
        """
        Test that an authenticated user can create a track with valid data.
        """
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        data = {
            "title": "Test Track",
            "description": "This is a test track.",
            "genre": "house",
            "audio_file": audio_file
        }
        response = self.client.post('/tracks/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Track.objects.count(), 1)
        track = Track.objects.first()
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.description, "This is a test track.")
        self.assertEqual(track.genre, "house")
        self.assertEqual(track.owner, self.profile)


    def test_create_track_unauthenticated(self):
        """
        Test that an unauthenticated user cannot create a track.
        """
        self.client.logout()

        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        data = {
            "title": "Test Track",
            "description": "This is a test track.",
            "genre": "house",
            "audio_file": audio_file
        }

        response = self.client.post('/tracks/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_track_missing_required_fields(self):
        """
        Test that the track creation API rejects missing required fields.
        """
        data = {
            "title": "Test Track",
            "description": "This is a test track.",
            "genre": "house"
        }
    
        response = self.client.post('/tracks/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('audio_file', response.data)
        self.assertEqual(response.data['audio_file'], ['No file was submitted.'])

from django.contrib.auth.models import User
from profiles.models import Profile
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Track
from django.core.files.uploadedfile import SimpleUploadedFile

class TrackTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Now assign the user directly to the track owner field, not the profile
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        self.track = Track.objects.create(
            owner=self.user,  # Directly assign the user to the owner field
            title="Test Track",
            genre="house",
            audio_file=audio_file
        )

    def test_create_track(self):
        """
        Test that an authenticated user can create a track with valid data.
        """
        # Ensure no tracks are present before the test
        Track.objects.all().delete()

        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        data = {
            "title": "Test Track",
            "description": "This is a test track.",
            "genre": "house",
            "audio_file": audio_file
        }
        response = self.client.post('/tracks/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that only one track was created
        self.assertEqual(Track.objects.count(), 1)
        track = Track.objects.first()
        self.assertEqual(track.title, "Test Track")
        self.assertEqual(track.description, "This is a test track.")
        self.assertEqual(track.genre, "house")
        self.assertEqual(track.owner, self.user)  # Change to self.user instead of self.profile

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

    def test_create_track_invalid_audio_format(self):
        """
        Test that an invalid audio file format (e.g., .mp4) is rejected.
        """
        audio_file = SimpleUploadedFile("test_audio.mp4", b"file_content", content_type="video/mp4")
        data = {
            "title": "Test Track",
            "description": "This is a test track.",
            "genre": "house",
            "audio_file": audio_file
        }
        response = self.client.post('/tracks/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('audio_file', response.data)
        self.assertEqual(response.data['audio_file'], ['Invalid audio file format!'])

    def test_create_track_missing_optional_fields(self):
        """
        Test that a track can be created without optional fields (album_cover, description).
        """
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        data = {
            "title": "Test Track Without Optional Fields",
            "genre": "house",
            "audio_file": audio_file
        }
        response = self.client.post('/tracks/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        track = Track.objects.first()
        self.assertIsNone(track.description)
        self.assertEqual(track.album_cover, '../default_cover')

    def test_create_track_audio_file_size_limit(self):
        """
        Test that track creation is rejected if the audio file exceeds the 100MB size limit.
        """
        large_audio_file = SimpleUploadedFile(
            "large_audio.mp3", 
            b"file" * (1024 * 1024 * 101),
            content_type="audio/mpeg"
        )

        data = {
            "title": "Test Track with Large Audio File",
            "description": "This track has a large audio file.",
            "genre": "house",
            "audio_file": large_audio_file
        }
        response = self.client.post('/tracks/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('audio_file', response.data)
        self.assertEqual(
            response.data['audio_file'][0], 
            'Audio file size larger than 100MB!'
        )

    def test_update_track(self):
        """
        Test that an authenticated user can update a track's details.
        """
        audio_file = SimpleUploadedFile("test_audio.mp3", b"file_content", content_type="audio/mpeg")
        data = {
            "title": "Original Track Title",
            "description": "Original description",
            "genre": "house",
            "audio_file": audio_file
        }
        response = self.client.post('/tracks/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        track = Track.objects.first()

        updated_audio_file = SimpleUploadedFile("updated_audio.mp3", b"new_file_content", content_type="audio/mpeg")
        updated_data = {
            "title": "Updated Track Title",
            "description": "Updated description",
            "genre": "tech_house",
            "audio_file": updated_audio_file
        }

        response = self.client.put(f'/tracks/{track.id}/', updated_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        track.refresh_from_db()
        self.assertEqual(track.title, "Updated Track Title")
        self.assertEqual(track.description, "Updated description")
        self.assertEqual(track.genre, "tech_house")

    def test_delete_track_authenticated(self):
        """
        Test that an authenticated user can delete a track.
        """
        response = self.client.delete(f'/tracks/{self.track.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Track.objects.count(), 0)

    def test_delete_track_unauthenticated(self):
        """
        Test that an unauthenticated user cannot delete a track.
        """
        self.client.logout()
        response = self.client.delete(f'/tracks/{self.track.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Track.objects.count(), 1)

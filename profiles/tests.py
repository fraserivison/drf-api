from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from profiles.models import Profile

class ProfileTests(APITestCase):
    def setUp(self):
        # Set up test data
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        
        # Ensure the profile is created for the user only if it doesn't already exist
        if not Profile.objects.filter(owner=self.user).exists():
            self.profile = Profile.objects.create(owner=self.user)
        else:
            self.profile = Profile.objects.get(owner=self.user)
        
        self.client = APIClient()

    def test_owner_can_update_own_profile(self):
        # Log in as the profile owner
        self.client.login(username='testuser', password='password123')

        # Update the profile data
        updated_data = {
            'dj_name': 'New DJ Name',
            'bio': 'Updated bio content.',
        }

        response = self.client.patch(f'/profiles/{self.profile.id}/', updated_data, format='json')

        # Check if the profile is updated
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.dj_name, 'New DJ Name')
        self.assertEqual(self.profile.bio, 'Updated bio content.')

    def test_non_owner_cannot_update_profile(self):
        # Log in as a non-owner
        self.client.login(username='otheruser', password='password123')

        # Attempt to update the profile
        updated_data = {
            'dj_name': 'Hacked DJ Name',
            'bio': 'Hacked bio content.',
        }

        response = self.client.patch(f'/profiles/{self.profile.id}/', updated_data, format='json')

        # Check if the profile update is forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_is_created_when_user_is_created(self):
        # Create a new user
        user = User.objects.create_user(username='newuser', password='password123')

        # Check if a profile is automatically created
        profile = Profile.objects.get(owner=user)
        self.assertEqual(profile.owner, user)

    def test_user_can_retrieve_own_profile(self):
        # Log in as the user
        self.client.login(username='testuser', password='password123')

        # Retrieve the profile
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')

        # Check if the profile is returned correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')

    def test_user_can_retrieve_another_users_profile(self):
        # Log in as a different user
        self.client.login(username='otheruser', password='password123')

        # Attempt to retrieve the profile of testuser
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')

        # Check that the response status is OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)









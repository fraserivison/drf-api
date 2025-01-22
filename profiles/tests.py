"""
Tests for the profile-related functionality in the profiles app.

This file contains test cases to verify the correct behavior of profile
creation, retrieval, and updates for users in the system.
"""

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from profiles.models import Profile

class ProfileTests(APITestCase):
    """
    Test cases for the Profile model and related views.

    This class includes tests to ensure that users can:
    - Update their own profile
    - Not update another user's profile
    - Retrieve their own profile
    - Retrieve another user's profile
    - A profile is automatically created when a user is created
    """
    def setUp(self):
        """
        Set up the test environment, creating users and profiles for testing.

        This method creates two users, one for testing profile updates
        and another for testing restricted access.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')

        if not Profile.objects.filter(owner=self.user).exists():
            self.profile = Profile.objects.create(owner=self.user)
        else:
            self.profile = Profile.objects.get(owner=self.user)

        self.client = APIClient()

    def test_owner_can_update_own_profile(self):
        """
        Test that a user can update their own profile.

        This test ensures that the logged-in user can update their profile
        information, such as the DJ name and bio.
        """
        self.client.login(username='testuser', password='password123')

        updated_data = {
            'dj_name': 'New DJ Name',
            'bio': 'Updated bio content.',
        }

        response = self.client.patch(f'/profiles/{self.profile.id}/', updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.dj_name, 'New DJ Name')
        self.assertEqual(self.profile.bio, 'Updated bio content.')

    def test_non_owner_cannot_update_profile(self):
        """
        Test that a user cannot update another user's profile.

        This test verifies that users who are not the profile owner
        receive a permission error when attempting to update the profile.
        """
        self.client.login(username='otheruser', password='password123')

        updated_data = {
            'dj_name': 'Hacked DJ Name',
            'bio': 'Hacked bio content.',
        }

        response = self.client.patch(f'/profiles/{self.profile.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_is_created_when_user_is_created(self):
        """
        Test that a profile is automatically created when a user is created.

        This test ensures that when a new user is created, a corresponding profile
        is automatically created and linked to the user.
        """
        user = User.objects.create_user(username='newuser', password='password123')
        profile = Profile.objects.get(owner=user)
        self.assertEqual(profile.owner, user)

    def test_user_can_retrieve_own_profile(self):
        """
        Test that a user can retrieve their own profile.

        This test verifies that users can retrieve the details of their own profile.
        """
        self.client.login(username='testuser', password='password123')
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')

    def test_user_can_retrieve_another_users_profile(self):
        """
        Test that a user can retrieve another user's profile.

        This test verifies that users can retrieve the profile details of other users.
        """
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

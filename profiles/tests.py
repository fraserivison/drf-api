from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from profiles.models import Profile

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.other_user = User.objects.create_user(username='otheruser', password='password123')
        
        if not Profile.objects.filter(username=self.user).exists():
            self.profile = Profile.objects.create(username=self.user)
        else:
            self.profile = Profile.objects.get(username=self.user)
        
        self.client = APIClient()

    def test_username_can_update_own_profile(self):
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

    def test_non_username_cannot_update_profile(self):
        self.client.login(username='otheruser', password='password123')

        updated_data = {
            'dj_name': 'Hacked DJ Name',
            'bio': 'Hacked bio content.',
        }

        response = self.client.patch(f'/profiles/{self.profile.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_is_created_when_user_is_created(self):
        user = User.objects.create_user(username='newuser', password='password123')
        profile = Profile.objects.get(username=user)
        self.assertEqual(profile.username, user)

    def test_user_can_retrieve_own_profile(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_user_can_retrieve_another_users_profile(self):
        self.client.login(username='otheruser', password='password123')
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)









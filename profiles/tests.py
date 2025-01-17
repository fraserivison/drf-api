from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from profiles.models import Profile

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(owner='testuser', password='password123')
        self.other_user = User.objects.create_user(owner='otheruser', password='password123')
        
        if not Profile.objects.filter(owner=self.user).exists():
            self.profile = Profile.objects.create(owner=self.user)
        else:
            self.profile = Profile.objects.get(owner=self.user)
        
        self.client = APIClient()

    def test_owner_can_update_own_profile(self):
        self.client.login(owner='testuser', password='password123')

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
        self.client.login(owner='otheruser', password='password123')

        updated_data = {
            'dj_name': 'Hacked DJ Name',
            'bio': 'Hacked bio content.',
        }

        response = self.client.patch(f'/profiles/{self.profile.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_is_created_when_user_is_created(self):
        user = User.objects.create_user(owner='newuser', password='password123')
        profile = Profile.objects.get(owner=user)
        self.assertEqual(profile.owner, user)

    def test_user_can_retrieve_own_profile(self):
        self.client.login(owner='testuser', password='password123')
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['owner'], 'testuser')

    def test_user_can_retrieve_another_users_profile(self):
        self.client.login(owner='otheruser', password='password123')
        response = self.client.get(f'/profiles/{self.profile.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)









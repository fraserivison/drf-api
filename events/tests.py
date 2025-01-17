from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from events.models import Event
from datetime import datetime, timedelta

class EventTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(owner='testuser', password='testpass')
        self.client.login(owner='testuser', password='testpass')

        self.event = Event.objects.create(
            owner=self.user,
            name='Original Event',
            description='Original description.',
            genre='house',
            date=(datetime.now() + timedelta(days=1)),
            location='Original location'
        )

    def test_create_event(self):
        data = {
            'name': 'Test Event',
            'description': 'A test event.',
            'genre': 'house',
            'date': (datetime.now() + timedelta(days=1)).isoformat(),
            'location': 'Test Location'
        }

        response = self.client.post('/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        event = Event.objects.get(id=response.data['id'])
        self.assertEqual(event.owner.owner, 'testuser')

    def test_edit_event(self):
        updated_data = {
            'name': 'Updated Event',
            'description': 'Updated description.',
            'genre': 'techno',
            'date': (datetime.now() + timedelta(days=2)).isoformat(),
            'location': 'Updated location'
        }

        response = self.client.put(f'/events/{self.event.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.event.refresh_from_db()
        self.assertEqual(self.event.name, 'Updated Event')
        self.assertEqual(self.event.description, 'Updated description.')
        self.assertEqual(self.event.genre, 'techno')
        self.assertEqual(self.event.location, 'Updated location')

    def test_delete_event(self):
        response = self.client.delete(f'/events/{self.event.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Event.DoesNotExist):
            Event.objects.get(id=self.event.id)

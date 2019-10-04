import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from connection.models import Connection
from user.models import Advocate, CustomUser, Survivor


class ConnectionTest(APITestCase):
    survivor_attributes = {
        'username': 'some_survivor',
        'email': 'survivor@email.com',
        'password': 'some password',
        'device_token': 'ExponentPushToken[xxxxxxxxxxxxxxxxxxxxxx]'
    }

    advocate_attributes = {
        'username': 'some_advocate',
        'email': 'advocate@email.com',
        'password': 'some other password',
        'device_token': 'ExponentPushToken[yyyyyyyyyyyyyyyyyyyyyy]'
    }

    def setUp(self):
        self.survivor_id = self.create_survivor(self.survivor_attributes)
        self.advocate_id = self.create_advocate(self.advocate_attributes)

        self.set_token(self.survivor_attributes)

    def test_request(self):
        response = self.client.post(reverse('connection:connection-request'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, int))

    def test_single_acceptance(self):
        response = self.client.post(reverse('connection:connection-request'))

        self.set_token(self.advocate_attributes)

        response = self.client.post(
            reverse('connection:connection-accept'),
            data=json.dumps({
                'survivor_id': self.survivor_id,
                'connection_id': response.data
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_multiple_acceptance(self):
        response = self.client.post(reverse('connection:connection-request'))

        self.set_token(self.advocate_attributes)

        self.client.post(
            reverse('connection:connection-accept'),
            data=json.dumps({
                'survivor_id': self.survivor_id,
                'connection_id': response.data
            }),
            content_type='application/json'
        )

        advocate_attributes = {
            'username': 'some other advocate',
            'email': 'other_advocate@email.com',
            'password': 'some other password',
            'device_token': 'ExponentPushToken[zzzzzzzzzzzzzzzzzzzzzz]'
        }

        self.create_advocate(advocate_attributes)
        self.set_token(advocate_attributes)

        response = self.client.post(
            reverse('connection:connection-accept'),
            data=json.dumps({
                'survivor_id': self.survivor_id,
                'connection_id': response.data
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list(self):
        Connection.objects.create(survivor_id=self.survivor_id, advocate_id=self.advocate_id)

        response = self.client.get(
            reverse('connection:connection-list')
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        connection = next(iter(response.data))

        self.assertEqual(connection['survivor'], self.survivor_id)
        self.assertEqual(connection['advocate'], self.advocate_id)


    def set_token(self, attributes):
        response = self.client.post(
            reverse('token-obtain-pair'),
            data=json.dumps({
                'username': attributes['username'],
                'password': attributes['password']
            }),
            content_type='application/json'
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access']
        )

    def create_survivor(self, attributes):
        user = CustomUser.objects.create_user(
            username=attributes['username'],
            email=attributes['email'],
            password=attributes['password'],
            device_token=attributes['device_token']
        )

        return Survivor.objects.create(user=user).user_id

    def create_advocate(self, attributes):
        user = CustomUser.objects.create_user(
            username=attributes['username'],
            email=attributes['email'],
            password=attributes['password'],
            device_token=attributes['device_token']
        )

        return Advocate.objects.create(user=user).user_id

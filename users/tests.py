from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


# Create your tests here.

class UserTestCase(APITestCase):

    def setUp(self):
        pass

    def test_create_user(self):
        """ Тест создания пользователя """

        data = {
            "email": 'test@gmail.com',
            "password": 'python'
        }

        response = self.client.post(
            reverse('users:register'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            User.objects.all().count(),
            1
        )
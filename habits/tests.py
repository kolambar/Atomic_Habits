from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit, Schedule, Period
from users.models import User


# Create your tests here.


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com',
            password='password',
        )

        self.second_user = User.objects.create(
            email='second_test@user.com',
            password='password',
        )

        self.habit = Habit.objects.create(
            action='test action',
            is_it_rewarding_habit=False,
            time_to_done='01:00',
            owner=self.user,
            is_public=True,
        )

        #  непубличная привычка созданная другим юзером
        self.hidden_habit = Habit.objects.create(
            action='hidden test action',
            is_it_rewarding_habit=False,
            time_to_done='01:00',
            owner=self.second_user,
            is_public=False,
        )

        #  публичная привычка созданная другим юзером
        self.public_habit = Habit.objects.create(
            action='public test action',
            is_it_rewarding_habit=False,
            time_to_done='01:00',
            owner=self.second_user,
            is_public=True,
        )

        self.client.force_authenticate(user=self.user)

    def test_get_detail_habit(self):
        """ Тест просмотра одной привычки """

        response = self.client.get(
            reverse('habits:habit', kwargs={'pk': self.habit.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
                    response.json(),
            {
                        'id': self.habit.pk,
                        'action': 'test action',
                        'place': None,
                        'reward': None,
                        'is_it_rewarding_habit': False,
                        'time_to_done': '01:00:00',
                        'is_public': True,
                        'on_schedule': None,
                        'periodic': None,
                        'rewarding_habit': None,
                        'owner': self.user.pk
                    }
        )

    def test_update_habit(self):
        """ Тест изменения привычки """

        data = {
            "action": 'test action',
            "is_it_rewarding_habit": False,
            "time_to_done": '02:00',
            "is_public": True,
            "owner": self.user.pk
        }

        response = self.client.put(
            reverse('habits:habit', kwargs={'pk': self.habit.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
                    response.json(),
            {
                        'id': self.habit.pk,
                        'action': 'test action',
                        'place': None,
                        'reward': None,
                        'is_it_rewarding_habit': False,
                        'time_to_done': '00:02:00',
                        'is_public': True,
                        'on_schedule': None,
                        'periodic': None,
                        'rewarding_habit': None,
                        'owner': self.user.pk
                    }
        )

    def test_delete_habit(self):
        """ Тест удаления привычки """

        response = self.client.delete(
            reverse('habits:habit', kwargs={'pk': self.habit.pk})
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_create_habit(self):
        """ Тест создания привычки """

        data = {
            "action": 'second test action',
            "is_it_rewarding_habit": False,
            "time_to_done": '02:00',
            "is_public": True,
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse('habits:create_habit'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Habit.objects.all().count(),
            4
        )

    def test_list_user_habit(self):
        """ Тест просмотра списка привычек пользователя """

        response = self.client.get(
            reverse('habits:my_habits')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
                    response.json(),
            {
                'count': 1,
                'page_size': 5,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.habit.pk,
                        'action': 'test action',
                        'place': None,
                        'reward': None,
                        'is_it_rewarding_habit': False,
                        'time_to_done': '01:00:00',
                        'is_public': True,
                        'on_schedule': None,
                        'periodic': None,
                        'rewarding_habit': None,
                        'owner': self.user.pk
                    }
                ]
            }
        )

    def test_list_public_habit(self):
        """ Тест просмотра списка публичных привычек """

        response = self.client.get(
            reverse('habits:public_habits')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'count': 2,
                'page_size': 5,
                'next': None,
                'previous': None,
                'results': [
                    {
                        'id': self.habit.pk,
                        'action': 'test action',
                        'place': None,
                        'reward': None,
                        'is_it_rewarding_habit': False,
                        'time_to_done': '01:00:00',
                        'is_public': True,
                        'on_schedule': None,
                        'periodic': None,
                        'rewarding_habit': None,
                        'owner': self.user.pk
                    },
                    {
                        'id': self.public_habit.pk,
                        'action': 'public test action',
                        'place': None,
                        'reward': None,
                        'is_it_rewarding_habit': False,
                        'time_to_done': '01:00:00',
                        'is_public': True,
                        'on_schedule': None,
                        'periodic': None,
                        'rewarding_habit': None,
                        'owner': self.second_user.pk
                    }
                ]
            }
        )


class ScheduleTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com',
            password='password',
        )

        self.schedule = Schedule.objects.create(
            title='test schedule',
            sun='12:00:00',
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_get_detail_schedule(self):
        """ Тест просмотра одного расписания """

        response = self.client.get(
            reverse('habits:schedule', kwargs={'pk': self.schedule.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
                    response.json(),
            {
                        'id': self.schedule.pk,
                        'title': 'test schedule',
                        'mon': None,
                        'tue': None,
                        'wed': None,
                        'th': None,
                        'fri': None,
                        'sat': None,
                        'sun': '12:00:00',
                        'owner': self.user.pk
                    }
        )

    def test_update_schedule(self):
        """ Тест изменения расписания """

        data = {
            'title': 'test schedule',
            'mon': '12:00:00',
            'tue': '12:00:00',
            'wed': '12:00:00',
            'th': '12:00:00',
            'fri': '12:00:00',
            'sat': '12:00:00',
            'sun': '12:00:00',
            "owner": self.user.pk
        }

        response = self.client.put(
            reverse('habits:schedule', kwargs={'pk': self.schedule.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
                    response.json(),
            {
                        'id': self.schedule.pk,
                        'title': 'test schedule',
                        'mon': '12:00:00',
                        'tue': '12:00:00',
                        'wed': '12:00:00',
                        'th': '12:00:00',
                        'fri': '12:00:00',
                        'sat': '12:00:00',
                        'sun': '12:00:00',
                        'owner': self.user.pk
                    }
        )

    def test_delete_schedule(self):
        """ Тест удаления расписания """

        response = self.client.delete(
            reverse('habits:schedule', kwargs={'pk': self.schedule.pk})
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_create_schedule(self):
        """ Тест создания расписания """

        data = {
            'title': 'second test schedule',
            'sun': '12:00:00',
            'owner': self.user.pk
        }

        response = self.client.post(
            reverse('habits:create_schedule'),
            data=data
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Schedule.objects.all().count(),
            2
        )


class PeriodTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='test@user.com',
            password='password',
        )

        self.period = Period.objects.create(
            title='test period',
            period='12:00',
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_get_detail_period(self):
        """ Тест просмотра одной периодичности """

        response = self.client.get(
            reverse('habits:period', kwargs={'pk': self.period.pk})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
                    response.json(),
            {
                        'id': self.period.pk,
                        'title': 'test period',
                        'period': '12:00:00',
                        'start': None,
                        'end': None,
                        'last_event': None,
                        'owner': self.user.pk
                    }
        )

    def test_update_period(self):
        """ Тест изменения периода """

        data = {
            'title': 'test period',
            'period': '08:00:00',
            "owner": self.user.pk
        }

        response = self.client.put(
            reverse('habits:period', kwargs={'pk': self.period.pk}),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
                    response.json(),
            {
                        'id': self.period.pk,
                        'title': 'test period',
                        'period': '08:00:00',
                        'start': None,
                        'end': None,
                        'last_event': None,
                        'owner': self.user.pk
            }
        )

    def test_delete_period(self):
        """ Тест удаления периода """

        response = self.client.delete(
            reverse('habits:period', kwargs={'pk': self.period.pk})
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_create_period(self):
        """ Тест создания периода """

        data = {
            'title': 'second test period',
            'period': '08:00:00',
            "owner": self.user.pk
        }

        response = self.client.post(
            reverse('habits:create_period'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Period.objects.all().count(),
            2
        )

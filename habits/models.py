from django.db import models

from users.models import User

# Create your models here.


NULLABLE = {'blank': True, 'null': True}


class Schedule(models.Model):
    title = models.CharField(max_length=100, verbose_name='расписание')

    #  для настройки времени для каждого дня недели
    mon = models.TimeField(verbose_name='время для привычки в пн')
    tue = models.TimeField(verbose_name='время для привычки в вт')
    wed = models.TimeField(verbose_name='время для привычки в ср')
    th = models.TimeField(verbose_name='время для привычки в чт')
    fri = models.TimeField(verbose_name='время для привычки в пт')

    sat = models.TimeField(verbose_name='время для привычки в сб')
    sun = models.TimeField(verbose_name='время для привычки в вс')


class Period(models.Model):
    title = models.CharField(max_length=100, verbose_name='распорядок')

    period = models.DurationField(verbose_name='раз в какое количество часов')
    start = models.TimeField(verbose_name='время начала', **NULLABLE)  # время начала в каждые сутки
    end = models.TimeField(verbose_name='время окончания', **NULLABLE)  # время окончания в каждые сутки

    # отсчитывает period от последнего раза
    last_event = models.TimeField(verbose_name='время последнего выполнения', **NULLABLE)


class Habit(models.Model):
    action = models.CharField(max_length=100, verbose_name='действие', unique=True)
    place = models.CharField(max_length=100, verbose_name='место для привычки', **NULLABLE)

    # работает либо по расписанию, либо с интервалом
    on_schedule = models.ForeignKey(Schedule, on_delete=models.SET_NULL, verbose_name='расписание для привычки', **NULLABLE)
    periodic = models.ForeignKey(Period, on_delete=models.SET_NULL, verbose_name='периодичность привычки', **NULLABLE)

    reward = models.CharField(max_length=100, verbose_name='награда', **NULLABLE)
    is_it_rewarding_habit = models.BooleanField(verbose_name='это привычка поощрения')
    rewarding_habit = models.ForeignKey('Habit', on_delete=models.SET_NULL,
                                        verbose_name='связанная привычка поощрения', **NULLABLE)
    time_to_done = models.DurationField(verbose_name='время на выполнение привычки')

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель')
    is_public = models.BooleanField(verbose_name='видна другим пользователям')  # чтобы делиться привычкой с другими

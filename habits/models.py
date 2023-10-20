from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.db import models

from habits.validators import check_timings, check_reward_character
from users.models import User

# Create your models here.


NULLABLE = {'blank': True, 'null': True}


class Schedule(models.Model):
    title = models.CharField(max_length=100, verbose_name='расписание')

    #  для настройки времени для каждого дня недели
    mon = models.TimeField(verbose_name='время для привычки в пн', **NULLABLE)
    tue = models.TimeField(verbose_name='время для привычки в вт', **NULLABLE)
    wed = models.TimeField(verbose_name='время для привычки в ср', **NULLABLE)
    th = models.TimeField(verbose_name='время для привычки в чт', **NULLABLE)
    fri = models.TimeField(verbose_name='время для привычки в пт', **NULLABLE)

    sat = models.TimeField(verbose_name='время для привычки в сб', **NULLABLE)
    sun = models.TimeField(verbose_name='время для привычки в вс', **NULLABLE)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', null=True)

    def save(self, *args, **kwargs):
        if (not self.mon and not self.tue and not self.wed and not self.th and not self.fri
                and not self.sat and not self.sun):
            raise ValidationError("Schedule must have at least 1 day on week to work")

        super(Schedule, self).save(*args, **kwargs)


class Period(models.Model):
    title = models.CharField(max_length=100, verbose_name='распорядок')

    period = models.DurationField(
        verbose_name='раз в какое количество часов',
        validators=[MaxValueValidator(limit_value=timedelta(hours=24))],  # максимально день, для остального Schedule
    )
    start = models.TimeField(verbose_name='время начала', **NULLABLE)  # время начала в каждые сутки
    end = models.TimeField(verbose_name='время окончания', **NULLABLE)  # время окончания в каждые сутки

    # отсчитывает period от последнего раза
    last_event = models.TimeField(verbose_name='время последнего выполнения', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', null=True)


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
    time_to_done = models.DurationField(
        verbose_name='время на выполнение привычки',
        validators=[MaxValueValidator(limit_value=timedelta(minutes=2))],  # максимальное время на выполнение 2 мин
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель', null=True)
    is_public = models.BooleanField(verbose_name='видна другим пользователям')  # чтобы делиться привычкой с другими

    def save(self, *args, **kwargs):
        check_timings(self)
        check_reward_character(self)

        super(Habit, self).save(*args, **kwargs)

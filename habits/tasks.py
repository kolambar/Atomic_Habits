from datetime import datetime

from celery import shared_task

from config import settings

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from habits.models import Habit
from habits.services import send_tg_message, set_last_event

day_of_week = {
    0: 'mon',
    1: 'tue',
    2: 'wed',
    3: 'th',
    4: 'fri',
    5: 'sat',
    6: 'sun',
}


@shared_task
def task_check_schedules():
    """ Задача для отправки напоминаний о привычках, завязанных на расписанию"""
    current_day = datetime.today().weekday()  # получает день недели
    # получает время в часах и минутах в формате datetime.time
    time_with_minutes = datetime.strptime(datetime.today().strftime('%H:%M'), '%H:%M').time()

    # получает те привычки, которые связаны с объектом Schedule
    habits_on_schedule = Habit.objects.filter(on_schedule__isnull=False)

    for habit in habits_on_schedule:
        field_name = day_of_week.get(current_day)  # берет из словаря название поля соответствующее текущему дню недели
        # Проверяет, есть ли у этого Schedule поле, отвечающее за этот день недели. Если есть то получает его значени
        if hasattr(habit.on_schedule, field_name):
            field_value = getattr(habit.on_schedule, field_name)

            # Сравнивает
            if field_value == time_with_minutes:
                send_tg_message(habit, settings.TELEGRAM_TOKEN)


@shared_task
def task_check_periods():
    """ Задача для отправки напоминаний о привычках, завязанных на периодичности"""
    exact_moment = datetime.today()

    # получает те привычки, которые связаны с объектом Habit
    periodic_habits = Habit.objects.filter(periodic__isnull=False)
    for habit in periodic_habits:

        period = habit.periodic
        # проверяет рабочее ли это время для этого расписания
        if period.start < exact_moment.time() < period.end:
            # проверяет, отправлялось ли уведомление
            if not period.last_event:
                send_tg_message(habit, settings.TELEGRAM_TOKEN)
                set_last_event(period, exact_moment)
            else:
                # проверяет, что прошло достаточно времени после прошлой отправки
                if exact_moment - datetime.combine(datetime.today(), period.last_event) >= period.period:
                    send_tg_message(habit, settings.TELEGRAM_TOKEN)
                    set_last_event(period, exact_moment)

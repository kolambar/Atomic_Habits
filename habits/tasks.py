from datetime import datetime
from config import settings

import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from habits.models import Habit, Schedule
from habits.services import send_tg_message


day_of_week = {
    0: Schedule.mon,
    1: Schedule.tue,
    2: Schedule.wed,
    3: Schedule.th,
    4: Schedule.fri,
    5: Schedule.sat,
    6: Schedule.sun,

}


def task_check_schedules():
    print('asd')
    current_day = datetime.today().weekday()
    time_with_minutes = datetime.strptime(datetime.today().strftime('%H:%M'), '%H:%M').time()

    habits_on_schedule = Habit.objects.filter(on_schedule__isnull=False)

    print(habits_on_schedule)
    for habit in habits_on_schedule:
        print(habit.on_schedule.day_of_week[current_day])
        # проверяет, пришло ли время отправлять
        if habit.on_schedule.day_of_week[current_day] == time_with_minutes:
            send_tg_message(habit, settings.TELEGRAM_TOKEN)


def task_check_periods():
    exact_moment = datetime.today()

    periodic_habits = Habit.objects.filter(periodic__isnull=False)
    for habit in periodic_habits:

        period = habit.period
        # проверяет рабочее ли это время для этого расписания
        if period.start < exact_moment < period.end:

            # проверяет, отправлялось ли уведомление
            if not period.last_event:
                send_tg_message(habit, settings.TELEGRAM_TOKEN)
            else:
                # проверяет, что прошло достаточно времени после прошлой отправки
                if exact_moment - datetime.combine(datetime.today(), period.last_event) >= period.period:
                    send_tg_message(habit, settings.TELEGRAM_TOKEN)


if __name__ == '__main__':

    task_check_schedules()

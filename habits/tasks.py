from datetime import datetime
from config import settings
from habits.models import Habit, Schedule
from habits.services import create_message
from telegram_bot.send_message_bot import send_tg_message

day_of_week = {
    0: Schedule.mon,
    1: Schedule.tue,
    2: Schedule.wed,
    3: Schedule.th,
    4: Schedule.fri,
    5: Schedule.sat,
    6: Schedule.sun,

}


def check_schedules():
    current_day = datetime.today().weekday()
    time_with_minutes = datetime.strptime(datetime.today().strftime('%H:%M'), '%H:%M').time()

    habits_on_schedule = Habit.objects.filter(on_schedule__isnull=False)
    for habit in habits_on_schedule:
        # проверяет, пришло ли время отправлять
        if habit.on_schedule.day_of_week[current_day] == time_with_minutes:
            message = create_message(habit)
            send_tg_message(settings.TELEGRAM_TOKEN, habit.owner.telegram_id, message)


def check_periods():
    exact_moment = datetime.today()

    periodic_habits = Habit.objects.filter(periodic__isnull=False)
    for habit in periodic_habits:

        period = habit.period
        # проверяет рабочее ли это время для этого расписания
        if period.start < exact_moment < period.end:

            # проверяет, отправлялось ли уведомление
            if not period.last_event:
                message = create_message(habit)
                send_tg_message(settings.TELEGRAM_TOKEN, habit.owner.telegram_id, message)
            else:
                # проверяет, что прошло достаточно времени после прошлой отправки
                if exact_moment - datetime.combine(datetime.today(), period.last_event) >= period.period:
                    message = create_message(habit)
                    send_tg_message(settings.TELEGRAM_TOKEN, habit.owner.telegram_id, message)

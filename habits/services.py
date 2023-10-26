import asyncio

from habits.models import Habit
from telegram_bot.send_message_bot import send_to_tg


def create_message(habit: Habit):
    """
    Функция получает привычку и делает из нее сообщение для напоминания призыва к действию
    :param habit:
    :return:
    """
    call_to_act = f'Время для привычки {habit.action} в месте {habit.place}. Время на выполнение {habit.time_to_done}\n'

    # За полезной привычкой следует либо вознаграждение, либо приятная привычка
    if habit.reward:
        call_to_act += f'После привычки вас ждет {habit.reward}!'
    else:
        call_to_act += f'После привычки вас ждет {habit.rewarding_habit.action}!'

    return call_to_act


def send_tg_message(habit, token):
    """ Объединяет в себе функции"""
    message = create_message(habit)
    asyncio.run(send_to_tg(token, habit.owner.telegram_id, message))


def set_last_event(period, exact_moment):
    period.last_event = exact_moment
    period.save()

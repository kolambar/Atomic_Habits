from habits.models import Habit
from telegram_bot.send_message_bot import send_to_tg


def create_message(habit: Habit):
    """
    Функция получает привычку и делает из нее сообщение для напоминания за 15 мин и сообщение для призыва к действию
    :param habit:
    :return:
    """
    reminder_message = f'Через 15 минут наступит время привычки {habit.action}. Место - {habit.place}'
    call_to_act = f'Время для привычки {habit.action} в месте {habit.place}. Время на выполнение {habit.time_to_done}\n'

    # За полезной привычкой следует либо вознаграждение, либо приятная привычка
    if habit.reward:
        call_to_act += f'После привычки вас ждет {habit.reward}!'
    else:
        call_to_act += f'После привычки вас ждет {habit.rewarding_habit}!'

    return reminder_message, call_to_act


def send_tg_message(habit, token):
    message = create_message(habit)
    send_to_tg(token, habit.owner.telegram_id, message)

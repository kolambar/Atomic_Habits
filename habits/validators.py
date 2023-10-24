from django.core.exceptions import ValidationError


def check_timings(value):
    """
    Проверяет, что у привычки есть только один вид расписания (on_schedule или periodic)
    :param value:
    :return:
    """
    if value.on_schedule and value.periodic:
        raise ValidationError("Привычка может работать либо по расписанию либо с интервалом.")


def check_reward_character(value):
    """
    Проверяет: привычка, либо сама по себе поощряющая, либо есть поощрение или связанная привычка, которая поощряет.
    Все три поля могут быть пустыми.
    :param value:
    :return:
    """
    if bool(value.reward) + bool(value.is_it_rewarding_habit) + bool(value.rewarding_habit) > 1:
        raise ValidationError("Вознаграждение, признак вознаграждающей привычки, ссылка на вознаграждающую привычку"
                              " - только одно из этих полей может быть заполнено.")


def check_rewarding_habit(value):
    """
    Проверяет, что связанная привычка является поощряющей, а не atomic
    :param value:
    :return:
    """
    if value.rewarding_habit:
        if not value.rewarding_habit.is_it_rewarding_habit:
            raise ValidationError("Нельзя в качестве поощряющей привычки выбрать обычную.")

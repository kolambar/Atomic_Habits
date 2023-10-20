from django.core.exceptions import ValidationError


def check_timings(self):
    """
    Проверяет, что у привычки есть только один вид расписания (on_schedule или periodic)
    :param self:
    :return:
    """
    if self.on_schedule and self.periodic:
        raise ValidationError("Both on_schedule and periodic can't be set at the same time.")


def check_reward_character(self):
    """
    Проверяет: привычка, либо сама по себе поощряющая, либо есть поощрение или связанная привычка, которая поощряет.
    Все три поля могут быть пустыми.
    :param self:
    :return:
    """
    if bool(self.reward) + bool(self.is_it_rewarding_habit) + bool(self.rewarding_habit) > 1:
        raise ValidationError("reward, is_it_rewarding_habit and rewarding_habit can't be set at the same time.")

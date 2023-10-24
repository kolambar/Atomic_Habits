from django.urls import path

from habits.apps import HabitsConfig
from habits.views.habits import PublicHabitListView, HabitListView, HabitCreateView, HabitView
from habits.views.timings import ScheduleCreateView, PeriodCreateView, ScheduleView, PeriodView

app_name = HabitsConfig.name


urlpatterns = [
    # адреса страниц для работы с расписаниями
    path('create_schedule/', ScheduleCreateView.as_view(), name='create_schedule'),
    path('<int:pk>/', ScheduleView.as_view(), name='schedule'),

    # адреса страниц для работы с периодами
    path('create_period/', PeriodCreateView.as_view(), name='create_period'),
    path('period/<int:pk>/', PeriodView.as_view(), name='period'),

    # адреса страниц для работы с привычками
    path('', PublicHabitListView.as_view(), name='public_habits'),
    path('my/', HabitListView.as_view(), name='my_habits'),
    path('create_habit/', HabitCreateView.as_view(), name='create_habit'),
    path('habit/<int:pk>/', HabitView.as_view(), name='habit'),
]

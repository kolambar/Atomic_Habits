from django.urls import path

from habits.apps import HabitsConfig
from habits.views.habits import PublicHabitListView, HabitListView, HabitCreateView, HabitView
from habits.views.timings import ScheduleCreateView, PeriodCreateView, ScheduleUpdateView, ScheduleDeleteView, \
    PeriodUpdateView, PeriodDeleteView

app_name = HabitsConfig.name


urlpatterns = [
    # адреса страниц для работы с расписаниями
    path('create_schedule/', ScheduleCreateView.as_view(), name='create_schedule'),
    path('update_schedule/<int:pk>/', ScheduleUpdateView.as_view(), name='update_schedule'),
    path('delete_schedule/<int:pk>/', ScheduleDeleteView.as_view(), name='delete_schedule'),

    # адреса страниц для работы с периодами
    path('create_period/', PeriodCreateView.as_view(), name='create_period'),
    path('update_period/<int:pk>/', PeriodUpdateView.as_view(), name='update_period'),
    path('delete_period/<int:pk>/', PeriodDeleteView.as_view(), name='delete_period'),

    # адреса страниц для работы с привычками
    path('', PublicHabitListView.as_view(), name='public_habits'),
    path('my/', HabitListView.as_view(), name='my_habits'),
    path('create_habit/', HabitCreateView.as_view(), name='create_habit'),
    path('habit/<int:pk>/', HabitView.as_view(), name='habit'),
]

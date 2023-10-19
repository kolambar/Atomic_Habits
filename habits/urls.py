from django.urls import path

from habits.apps import HabitsConfig
from habits.views.timings import ScheduleCreateView, PeriodCreateView

app_name = HabitsConfig.name


urlpatterns = [
    path('create_schedule/', ScheduleCreateView.as_view(), name='create_schedule'),
    path('create_period/', PeriodCreateView.as_view(), name='create_period'),
]

from django.contrib import admin

from habits.models import Habit, Schedule, Period


# Register your models here.


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('action', 'on_schedule', 'periodic', )
    search_fields = ('action', 'on_schedule', 'periodic', )


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'mon', 'tue', 'wed', 'th', 'fri', 'sat', 'sun', )
    search_fields = ('title', )


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('title', 'period', 'start', 'end', 'last_event', )
    search_fields = ('title', )

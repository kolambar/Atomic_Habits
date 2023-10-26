from rest_framework import serializers

from habits.models import Schedule, Period


class ScheduleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Schedule
        fields = '__all__'


class PeriodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Period
        fields = '__all__'

from rest_framework.generics import UpdateAPIView, CreateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from habits.models import Schedule, Period
from habits.permissions import IsOwner
from habits.serializers.timings import ScheduleSerializer, PeriodSerializer


class ScheduleCreateView(CreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ScheduleView(RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsOwner]


class PeriodCreateView(CreateAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PeriodView(RetrieveUpdateDestroyAPIView):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = [IsOwner]

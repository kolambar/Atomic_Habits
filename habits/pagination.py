from rest_framework.pagination import PageNumberPagination


class HabitsPagination(PageNumberPagination):
    page_size = 5

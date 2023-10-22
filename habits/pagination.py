from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class HabitsPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('page_size', self.page_size),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductSetPagination(PageNumberPagination):
    page_size = 1

    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'page': self.page.number,
                'has_prev': self.page.has_previous(),
                'has_next': self.page.has_next(),
                'total_pages': self.page.paginator.num_pages,
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'data': data
        })

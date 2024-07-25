from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class NeatPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10
    page_size_query_param = 'limit'

    def get_paginated_response(self, data):
        current_page = self.page.number
        paginator = self.page.paginator

        return Response({
            'pagination': {
                'current_page': current_page,
                'items_count': paginator.count,
                'pages_count': paginator.num_pages,
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link(),
                'has_previous': self.page.has_previous(),
                'has_next': self.page.has_next()
            },
            'results': data
        })

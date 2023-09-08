from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100


    def get_paginated_response(self, data):
        request = self.request
        response_data = {
            'message': None,
            'status': "OK",
            'data': {
                request.resolver_match.url_name: data
            },
            'paginator': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            }
        }
        return Response(response_data)

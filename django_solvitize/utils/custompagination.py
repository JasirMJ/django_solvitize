import re
from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
    def get_paginated_response(self, data):
        lastpage = str(self.page.paginator.num_pages)
        first, last = None, None

        next_link = self.get_next_link()
        prev_link = self.get_previous_link()

        if next_link:
            last = re.sub(r'page=\d+', f'page={lastpage}', next_link)
        if prev_link:
            first = re.sub(r'page=\d+', 'page=1', prev_link)

        return Response({
            'next': next_link,
            'previous': prev_link,
            'first_page': first,
            'last_page': last,
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data
        })

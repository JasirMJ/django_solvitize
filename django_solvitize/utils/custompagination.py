from rest_framework import pagination
from rest_framework.response import Response
import re

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        lastpage = str(self.page.paginator.num_pages)
        first,last = None,None

        if self.get_next_link():
            last = str(re.sub(r'page=\d', 'page='+lastpage, self.get_next_link()))
        if self.get_previous_link():
            first = str(re.sub(r'page=\d', 'page=1', self.get_previous_link()))

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'first_page': first,
            'last_page': last,
            'count': self.page.paginator.count,
            'num_pages':self.page.paginator.num_pages,
            'current_page':self.page.number,
            'results': data
        })
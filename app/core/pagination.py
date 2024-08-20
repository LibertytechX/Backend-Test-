from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status

class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response(
            {
                'data': {
                    'next': self.get_next_link(),
                    'previous': self.get_previous_link(),
                    'count': len(data),
                    'total_count': self.count,
                    'results': data
                },
                'message' : 'Items retrived successfully'
            },
            status=status.HTTP_200_OK
        )
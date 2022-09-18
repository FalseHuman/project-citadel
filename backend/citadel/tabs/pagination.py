from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        max_sum = 0
        min_sum = 0
        date = self.request.query_params.get('date').split('-')
        new_data = self.request.user.pays.filter(data__year=date[0], data__month=date[1])
        for i in range(len(new_data)):
            if new_data[i].cost > 0:
                max_sum += new_data[i].cost
            else:
                min_sum += new_data[i].cost
        print(max_sum, min_sum)
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'income': max_sum,
            'expense': min_sum,
            'total': max_sum + min_sum,
            'results': data
        })
from rest_framework.pagination import PageNumberPagination as BasePageNumberPagination
from rest_framework.response import Response


class PageNumberPagination(BasePageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 50
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "result": data,
                "pagination": {
                    "next": self.page.has_next(),
                    "previous": self.page.has_previous(),
                    "count": self.page.paginator.count,
                    "page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "page_size": self.get_page_size(self.request),
                },
            }
        )

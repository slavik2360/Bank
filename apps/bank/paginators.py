# DRF
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList


class TransactionPageNumberPaginator(PageNumberPagination):
    """
    Пагинатор для вывода истории транзации.

    Параметры:
        - page_size_query_param:
        Параметр для того чтоб указывать сколько нужно вывести элементов

        - page_query_param:
        Параметр для того чтоб указывать нумерацию страницы

        - max_page_size:
        сколько максимум можно вывести элементов

        - page_size:
        по стандарту сколько будет элементов

    Пример запроса:
        api/v1/transactions/?page=2&size=10
    """
    page_size_query_param: str = 'size'
    page_query_param: str = 'page'
    max_page_size: int = 10
    page_size: int = 10

    def get_paginated_response(
        self,
        data: ReturnList
    ) -> Response:
        response: Response = \
            Response(
                {
                    'pagination': {
                        'next': self.get_next_link(),
                        'previous': self.get_previous_link(),
                        'pages': self.page.paginator.num_pages,
                        'count': self.page.paginator.count
                    },
                    'results': data
                }
            )
        return response
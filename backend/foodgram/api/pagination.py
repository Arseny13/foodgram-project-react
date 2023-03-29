from rest_framework.pagination import PageNumberPagination


class PageNumberAsLimitOffset(PageNumberPagination):
    page_size_query_param = "limit"

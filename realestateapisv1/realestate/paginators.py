from rest_framework.pagination import PageNumberPagination

class ArticlePaginator(PageNumberPagination):
    page_size=10
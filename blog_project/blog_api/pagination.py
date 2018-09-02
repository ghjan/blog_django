# _*_ coding: utf-8 _*_


# 自定义 Pagination，每个 Pagination 的属性不同，可以通过源码查看，然后修改需要的属性
from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page"

# _*_ coding: utf-8 _*_

import django_filters

# 自定义过滤器需要继承 django_filters.rest_framework.FilterSet 类来写
from blog.models import Post


class PostFilter(django_filters.rest_framework.FilterSet):
    # 定义进行过滤的参数，CharFilter 是过滤参数的类型，过滤器参数类型还有很多，包括
    # BooleanFilter，ChoiceFilter，DateFilter，NumberFilter，RangeFilter..等等
    # field_name 为筛选的参数名，需要和你 model 中的一致，lookup_expr 为筛选参数的条件
    # 例如 icontains 为 忽略大小写包含，例如 NumberFilter 则可以有 gte，gt，lte，lt，
    # year__gt，year__lt 等
    # title = django_filters.CharFilter('title', lookup_expr='icontains')
    sort = django_filters.OrderingFilter(fields=('create_time',))

    # 指定筛选的 model 和筛选的参数，其中筛选的参数在前面设置了筛选条件，则根据筛选条件来执行，
    # 如果为指定筛选条件，则按照精确查询来执行
    class Meta:
        model = Post
        fields = {
            'title': ['icontains']
        }

# _*_ coding: utf-8 _*_
from django import template
from blog.models import Category

# register 是 template.Library 的实例，是所有注册标签和过滤器的数据结构
register = template.Library()


# 自定义过滤器
@register.filter
def get_value(dic, key_name):
    return dic.get(key_name) if isinstance(dic, dict) else ''


@register.filter
def get_attr(d, m):
    if hasattr(d, m):
        return getattr(d, m) if isinstance(d, dict) else ''


# 自定义标签
@register.simple_tag
def get_all_category():
    return Category.objects.all()

# _*_ coding: utf-8 _*_
from django.conf.urls import url
from .views.blog import *
from .views.category import *
from .views.post import *

# 加上 app_name, 值同 include 中 namespace 的值，否则可能会找不到 url
app_name = 'blog'
urlpatterns = [
    # 当模版引用本地 url 时候需要用到 name 字段值，例如
    # <a href="{% url 'blog:home' %}"><b>Home</b></a>
    url(r'^home/$', home, name='home'),
    # url(r'^home/$', HomeView.as_view(), name='home'),
    # url(r'cate/(?P<pk>[0-9]+)/$', views.category, name='cate'),
    url(r'cate/(?P<pk>[0-9]+)/$', CategoryView.as_view(), name='category'),
    # url(r'post/(?P<pk>[0-9]+)/$', views.post_detail, name='post'),
    url(r'post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),

    # ?P<offset> 为传递的参数字段名，紧随其后的是参数值的匹配正则
    # 可以通过 http://localhost:8000/time/ahead/(offset)/ 来访问相应网址
    url(r'^time/ahead/(?P<offset>\d{1,2})/$', hours_ahead, name="time_ahead"),
    url(r'^post/new/$', new_post, name='new_post'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^full/$', FullPostView.as_view(), name='full'),
    url(r'^about/$', about, name='about'),
    url(r'^search/$', search, name='search'),

    url(r'^tag/(?P<pk>[0-9]+)/$', tags, name='tags'),
    # url(r'^tag/(?P<pk>[0-9]+)/$', views.TagView.as_view(), name='tags'),

]

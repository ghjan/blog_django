# _*_ coding: utf-8 _*_
from django.conf.urls import url
from . import views

# 加上 app_name, 值同 include 中 namespace 的值，否则可能会找不到 url
app_name = 'blog'
urlpatterns = [
    # 当模版引用本地 url 时候需要用到 name 字段值，例如
    # <a href="{% url 'blog:home' %}"><b>Home</b></a>
    url(r'^home$', views.home, name='home'),
    # ?P<offset> 为传递的参数字段名，紧随其后的是参数值的匹配正则
    # 可以通过 http://localhost:8000/time/ahead/(offset)/ 来访问相应网址
    url(r'^time/ahead/(?P<offset>\d{1,2})/$', views.hours_ahead, name="time_ahead"),
    url(r'^index', views.index, name='index'),
    url(r'^post/new/$', views.new_post, name='new_post'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^full/$', views.FullPostView.as_view(), name='full'),
    url(r'^about/$', views.about, name='about'),
]

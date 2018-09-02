# _*_ coding: utf-8 _*_

# blog_api 下的 urls
from django.conf.urls import url
from . import views

# 必须加上，且同 project 下 urls 中的 namespace 同值
app_name = 'api'

urlpatterns = [
    url(r'^posts/$', views.post_list, name="api_posts"),
]

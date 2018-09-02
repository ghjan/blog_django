# _*_ coding: utf-8 _*_

# blog_api 下的 urls
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

# 必须加上，且同 project 下 urls 中的 namespace 同值
app_name = 'api'

urlpatterns = [
    url(r'^posts/$', views.PostListMixins.as_view(), name="api_posts"),
    url(r'^post/(?P<pk>\d+)/$', views.PostDetailMixin.as_view(), name='api_post'),
]
# 增加这一行，这样我们就不需要逐一地添加对格式支持的 url 样式
urlpatterns = format_suffix_patterns(urlpatterns)

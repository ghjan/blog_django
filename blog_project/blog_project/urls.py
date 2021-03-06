# _*_ coding: utf-8 _*_

# 在项目下 urls.py 文件配置应用的 urls.py 文件
from django.conf.urls import url, include
from django.contrib import admin
from blog_api.urls import router as blog_api_router

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # include 作用：在 django 匹配 url 时候匹配完 blog/ 后，再次匹配下层地址，所以在 blog/
    # 后面不可以添加 "$" 符号，不然会导致不能匹配到地址，namespace 为了区分不同应用下同名的模版
    url(r'^blog/', include('blog.urls', namespace="blog")),
    url(r'^comment/', include('comment.urls', namespace="comment")),
    # 配置 blog_api 的 url
    url(r'^api/', include(blog_api_router.urls)),

]

# _*_ coding: utf-8 _*_
from rest_framework import generics
from rest_framework import mixins

from blog.models import Post
from .serializers import PostSerializer


class PostListMixins(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    # 指定列表
    queryset = Post.objects.all()
    # 指定序列化类
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        # list 方法继承 ListModelMixin 而来
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # create 方法继承 CreateModelMixin 而来
        return self.create(self, request, *args, **kwargs)


# detail 视图通过 mixins 和 generics 改造
class PostDetailMixin(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(self, request, *args, **kwargs)

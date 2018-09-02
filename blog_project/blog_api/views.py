# _*_ coding: utf-8 _*_
from rest_framework import generics

from blog.models import Post
from .serializers import PostSerializer


# 列表视图
class PostListView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# detail 视图
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# _*_ coding: utf-8 _*_

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from blog.models import Post
from .serializers import PostSerializer


# 将该视图的请求方法写在注解中，表示该接口只接受列表内的请求方式
@api_view(['GET', 'POST'])
def post_list(request, format=None):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        # 通过 Response 展示相应的数据
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 引入 status 模块，比数字标识符更加直观
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def post_detail(request, pk, format=None):
    # 根据 pk 值获取对应的 post 实例
    post = get_object_or_404(Post, pk=pk)
    # 首先判断是否存在这个 post，不存在直接返回 404 NOT FOUND
    # 如果 settings.py 下的 DEBUG 属性设置为 True 的话，django 会不展示 404 页面，设置成 False 即可
    if post is None:
        return HttpResponse(status=404)
    # 如果 request 是 GET 方法，则直接展示对应 pk 的 post
    if request.method == 'GET':
        serializer = PostSerializer(post)
        # 将序列化后的数据转换成 json 展示
        return Response(serializer.data)
    # 如果 request 是 PUT 方法，则解析 request 中的参数，
    # 进行校验是否合理，合理则更新，否则返回 400 BAD REQUEST
    elif request.method == 'PUT':
        data = JSONParser().parser(request)
        # 更新 post 的值
        serializer = PostSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # 如果 request 是 DELETE 方法，则直接删除
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

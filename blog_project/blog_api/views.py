# _*_ coding: utf-8 _*_

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from .models import Post
from .serializers import PostModelSerializer


@csrf_exempt
def post_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostModelSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":
        # 将 request 中的参数取出来进行序列化
        data = JSONParser().parse(request)
        serializer = PostModelSerializer(data=data)
        # 判断是否有效的数据
        if serializer.is_valid():
            # 有效数据保存，返回 201 CREATED
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        # 无效则返回 400 BAD_REQUEST
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def post_detail(request, pk):
    # 根据 pk 值获取对应的 post 实例
    post = get_object_or_404(Post, pk=pk)
    # 首先判断是否存在这个 post，不存在直接返回 404 NOT FOUND
    # 如果 settings.py 下的 DEBUG 属性设置为 True 的话，django 会不展示 404 页面，设置成 False 即可
    if post is None:
        return HttpResponse(status=404)
    # 如果 request 是 GET 方法，则直接展示对应 pk 的 post
    if request.method == 'GET':
        serializer = PostModelSerializer(post)
        # 将序列化后的数据转换成 json 展示
        return JsonResponse(serializer.data)
    # 如果 request 是 PUT 方法，则解析 request 中的参数，
    # 进行校验是否合理，合理则更新，否则返回 400 BAD REQUEST
    elif request.method == 'PUT':
        data = JSONParser().parser(request)
        # 更新 post 的值
        serializer = PostModelSerializer(post, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    # 如果 request 是 DELETE 方法，则直接删除
    elif request.method == 'DELETE':
        post.delete()
        return HttpResponse(status=204)

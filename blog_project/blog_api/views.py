# _*_ coding: utf-8 _*_

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from .models import Post
from .serializers import PostSerializer


@csrf_exempt
def post_list(request):
    # 如果是 GET 请求则返回所有的列表
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    # 如果是 POST 请求则保存数据
    elif request.method == "POST":
        # 将 request 中的参数取出来进行序列化
        data = JSONParser().parse(request)
        serializer = PostSerializer(data=data)
        # 判断是否有效的数据
        if serializer.is_valid():
            # 有效数据保存，返回 201 CREATED
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        # 无效则返回 400 BAD_REQUEST
        return JsonResponse(serializer.errors, status=400)

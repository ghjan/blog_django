# _*_ coding: utf-8 _*_
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from blog.models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # 推荐重写该方法，默认返回 status.HTTP_204_NO_CONTENT，
    # 会返回空信息，个人觉得不方便判断，当然按照个人喜好决定
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post is not None:
            post.delete()
            return Response({"message": "delete succeed", "code": "200"},
                            status=status.HTTP_200_OK)
        return super(PostViewSet, self).destroy(self, request, *args, **kwargs)

    # 更新的时候，需要约定好 ManyToMany 字段的 id 回传时候以什么方式间隔，例如我们用 "," 分隔
    # 更新方法重写时候重写 perform_update 即可
    def perform_update(self, serializer):
        post = self.get_object()
        post.tags.clear()
        if self.request.data['tags']:
            if "," in self.request.data['tags']:
                for id in self.request.data['tags'].split(","):
                    post.tags.add(id)
            else:
                post.tags.add(self.request.data['tags'])
        serializer.save()

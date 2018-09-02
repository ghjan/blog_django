# _*_ coding: utf-8 _*_

from rest_framework import serializers
from blog.models import Post, Author, Tag


# serializer 类需要继承 serializers.Serializer，
# 然后实现父类的 update，create 方法
class PostSerializer(serializers.Serializer):
    # 声明需要被序列化和反序列化的字段，同 model 的字段，
    # 字段名注意需要同 model 字段同名
    title = serializers.CharField(max_length=70)
    body = serializers.CharField()
    create_time = serializers.DateTimeField()
    modified_time = serializers.DateTimeField()
    excerpt = serializers.CharField(max_length=200, allow_blank=True)

    # 定义创建方法
    def create(self, validated_date):
        return Post.objects.all()

    # 定义修改方法
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.create_time = validated_data.get('create_time', instance.create_time)
        instance.modified_time = validated_data.get('modified_time', instance.modified_time)
        instance.excerpt = validated_data.get('excerpt', instance.excerpt)


# # ModelSeralizer 会自动帮我们实现 update 和 create 方法
# class PostModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         # result 接口需要返回的字段，可以指定 "__all__" 展示全部参数
#         fields = ['title', 'body', 'create_time', 'modified_time', 'excerpt', 'category', 'tags', 'modified_time',
#                   'views']
#         # exclude 为不展示的字段名，和 fields author
#         # exclude = ['id', 'author']


# 然后我们需要给新增的 model 创建 serializer
class AuthorSerializer(serializers.ModelSerializer):
    # 会显示所有该 author 下的 posts
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = Author
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # ForeignKey 链表结构字段处理，有两种处理方式，第一种展示 serializer 中设置的字段，
    # 第二种展示某个指定字段
    # author = AuthorSerializer(read_only=True)
    author_name = serializers.ReadOnlyField(source="author.username")
    # ManyToMany 链表结构字段处理
    tag = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

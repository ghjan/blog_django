# _*_ coding: utf-8 _*_

from rest_framework import serializers
from .models import Post


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

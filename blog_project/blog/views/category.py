# _*_ coding: utf-8 _*_
import markdown
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from blog.models import Post, Category


# #################################################################################
# 获取特定条件下的模型数据
def category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=category)
    return render(request, 'blog/home.html', locals())


# 通过 ListView 类进行修改
# 基本属性同 HomeView 相同，也可以直接继承 HomeView 然后复写 get_queryset() 方法实现
# class CategoryView(ListView):
#     model = Post
#     template_name = 'blog/home.html'
#     context_objects_name = 'post_list'
#
#     # 该方法默认返回指定模型的全部数据，通过复写该方法，改变默认行为
#     def get_queryset(self, *args, **kwargs):
#         # 类视图中，从 url 捕获的命名组参数值保存在实例的 kwargs 中，是一个字典
#         # 非命名组参数值保存在实例的 args 中，是一个列表
#         category = get_object_or_404(Category, pk=kwargs.get('pk'))
#         return super(CategoryView, self).get_queryset().filter(category=category)

# #################################################################################


class CategoryView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'post_list'
    paginate_by = 10

    def get_queryset(self):
        category = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=category)

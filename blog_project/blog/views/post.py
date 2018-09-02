# _*_ coding: utf-8 _*_
import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.forms import PostForm
from blog.models import Post, Tag

# 获取相应模型下的全部数据
from blog_api.serializers import PostSerializer
from comment.forms import CommentForm


#
# def home(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/home.html', locals())

def home(request):
    limit = 1
    posts = Post.objects.all()
    paginator = Paginator(posts, limit)

    # 根据表单获取页码
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)  # 获取 num 页码下的列表
    except PageNotAnInteger:
        post_list = paginator.page(1)  # 如果 page 不是整数则返回第一页列表
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)  # 如果没有数据则返回最后一页列表

    return render(request, 'blog/home.html', locals())


# 通过 ListView 类来进行修改
class HomeView(ListView):
    model = Post  # 指定视图模型
    template_name = 'blog/home.html'  # 指定渲染的模版
    context_objects_name = 'post_list'  # 对应的模型列表数据保存的变量名


# #################################################################################
# 获取具体的详情
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.increase_views()
    post.body = markdown.markdown(post.body, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
    ])
    form = CommentForm()
    return render(request, 'blog/detail.html', locals())


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    # 返回一个 HttpResponse 实例，只有当 get 方法被调用后才有 self.object 属性，即 post 实例
    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 自增操作，self.object 的值即 post 对象
        self.object.increase_views()
        return response

    # 根据 post 的 pk 值获取相应的 post 实例
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        # 通过获取 post 实例进行相应渲染操作
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])

        post.body = md.convert(post.body)
        return post

    # 返回一个字典，为模版变量字典，传递给相应的模版
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update(locals())
        return context


def new_post(request):
    # Http 请求包括 POST 和 GET 两种，一般提交数据都是用 POST 请求
    # 因此当 request.method 为 POST 的时候才需要处理表单数据
    if request.method == 'POST':
        # 用户提交的信息存在 request.POST 中，相当于一个字典取值
        form = PostForm(request.POST)
        # 判断表单是否有效，django 自动校验表单数据是否合理，根据模型的字段类型来判断
        if form.is_valid():
            # commit=False 表示只生成模型类的实例，不马上保存到数据库
            post = form.save(commit=False)
            # 将作者和文章进行关联
            post.author = request.user
            # 通过调用 save() 方法将数据存入数据库
            post.save()
            # return render('post_detail', pk=post.pk)
            # 如果模型类中定义了 get_absolute_url 方法，可以用以下方式跳转
            # 会直接跳转 get_absolute_url 方法所指向的地址
            return redirect(post)
    else:
        # 如果不是 POST 重定向到空白的新建页面
        form = PostForm()
    return render(request, 'blog/post_new.html', locals())


class FullPostView(ListView):
    model = Post
    template_name = 'blog/full-width.html'
    context_object_name = 'post_list'
    paginate_by = 1


def search(request):
    # 获取到用户提交的搜索关键词，字典的键值同模版中的 name 属性值
    q = request.GET.get('q')
    error_message = ''
    # 根据 q 的值是否空设置相关信息
    if not q:
        error_message = 'Input Keyword'
        return render(request, 'blog/home.html', locals())

    # Q 对象用于包装查询表达式，其作用是为了提供复杂的查询逻辑
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/home.html', locals())


# ########################## TagPage ################################
def tags(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    post_list = Post.objects.filter(tags=tag)
    return render(request, 'blog/index.html', locals())


class TagView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "pot_list"
    paginate_by = 10

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag)


# ########################## ArchivesPage ############################
def archives(request, year):
    post_list = Post.objects.filter(create_time__year=year)
    return render(request, "blog/index.html", locals())


class ArchivesView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 10

    # 获取列表，该方法默认获取指定模型的全部列表数据，通过复写改变默认行为
    def get_queryset(self):
        # 在类视图中，从 URL 捕获的命名组参数值保存在实例的 kwargs 属性（是一个字典）里，
        # 非命名组参数值保存在实例的 args 属性（是一个列表）里
        year = self.kwargs.get('year')
        # 复写，指定筛选的条件，获取相应条件的列表
        return super(ArchivesView, self).get_queryset().filter(create_time__year=year)


# 由于指定的属性同 HomeView，也可以直接继承 HomeView
# 然后复写 get_queryset() 方法改变获取列表的默认行为达到相同效果
class ArchivesView2(HomeView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        return super(ArchivesView2, self).get_queryset().filter(create_time__year=year)


class PostList(APIView):
    # 定义 GET 请求的方法，内部实现相同 @api_view
    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 定义 POST 请求的方法
    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

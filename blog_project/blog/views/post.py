# _*_ coding: utf-8 _*_
import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from blog.forms import PostForm
from blog.models import Post, Tag

# 获取相应模型下的全部数据
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
    context_objects_name = 'post'

    # 方法返回一个 HttpResponse 实例
    def get(self, request, *args, **kwargs):
        # get 方法会通过调用 get_object 和 get_context——data 方法对模版渲染
        # def get(self, request, *args, **kwargs):
        # self.object = self.get_object()
        # context = self.get_context_data(object=self.object)
        # return self.render_to_response(context)
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        # 只有当 get 方法被调用后才有 self.object 属性，即 post 实例
        # 对应 post_detail 函数中的 post.increase_views()
        self.object.increase_views()
        return response

    # 根据 post 的 pk 值获取相应的 post 实例
    def get_object(self, queryset=None):
        post = super(PostDetailView, self).get_object(queryset=None)
        post.body = markdown.markdown(post.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        return post

    # 返回一个字典，为模版变量字典，传递给相应的模版
    def get_context(self, **kwargs):
        context = super(PostDetailView, self).get_context(**kwargs)
        form = CommentForm()
        # 更新 context 的内容，必须调用
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

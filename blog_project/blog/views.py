import datetime

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt

from blog.models import Post
from blog.forms import PostForm, ContactForm


def home(request):
    # context 中的参数名和模版中 {{ }} 包裹的相同
    post_list = Post.objects.all()

    title = "My Blog Home"
    welcome = "Welcome to My Blog"
    # return render(request, 'blog/home.html', context={
    #     'title': "My Blog Home",
    #     'welcome': "Welcome to My Blog"
    # })
    return render(request, 'blog/home.html', locals())


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except Exception as e:
        print(e)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("{} hours later is {}".format(offset, dt))


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


@csrf_exempt
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # 只打印查看提交的结果是否正确
            cd = form.cleaned_data
            print(cd)
            # 提交成功后跳转 home 页面，通过 spacename 和 name 值指定页面
            return redirect('blog:home')
    else:
        # 不是 POST 方式则重定向到空白页面
        form = ContactForm()
        # return render(request, 'blog/contact.html', None)
    return render(request, 'blog/contact.html', locals())


class FullPostView(ListView):
    model = Post
    template_name = 'blog/full-width.html'
    context_object_name = 'post_list'
    paginate_by = 10


def about(request):
    return render(request, 'blog/about.html', None)


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

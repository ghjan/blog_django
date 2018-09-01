import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from blog.forms import ContactForm


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except Exception as e:
        print(e)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("{} hours later is {}".format(offset, dt))


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


def about(request):
    return render(request, 'blog/about.html', None)

import datetime
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("Hello django")


def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except Exception as e:
        print(e)
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("{} hours later is {}".format(offset, dt))


def index(request):
    # context 中的参数名和模版中 {{ }} 包裹的相同
    return render(request, 'index.html', context={
        'title': "My Blog Home",
        'welcome': "Welcome to My Blog"
    })

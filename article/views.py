from urllib import response

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import fields
from django.db.models.fields import AutoField  # 引入作者模块
from django.http import (HttpResponse, HttpResponseRedirect, JsonResponse,
                         request)
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View

from .models import ArticlePost


class OrderView(LoginRequiredMixin,View):
    def get(self, request):
        return HttpResponse("you login in :get")

    def post(self, request):
        return HttpResponse("you login in :post")

class AsView(View):
    def get(self, request):
        return HttpResponse("get")

    def post(self, request):
        return HttpResponse("post")


def SetSession(request):
    username = request.GET.get("username")
    userid = 1

    request.session["user_id"] = userid
    request.session["username"] = username

    return HttpResponse("setsession!")


def GetSession(request):
    username = request.session.get("username")
    userid = request.session.get("user_id")

    content = 'userid={}</br>username={}'.format(userid, username)

    return HttpResponse(content)


def SetCookie(request):
    username = request.GET.get("username")
    res = HttpResponse("set cookie")
    # 注意是给返回的网页设置cookie,以下写法没有返回网页内容
    # res=HttpResponse.set_cookie("name", username)
    res.set_cookie("name", username)
    return res


def GetCookie(request):
    username = request.COOKIES.get("name")
    return HttpResponse(username)


# Create your views here.
def test(request, id1, id2):
    #获取GET的参数
    param = request.GET
    p1 = "no a" if param['a'] is None else param['a']
    p2 = "no b" if param['b'] is None else param['b']
    res = f"id1={id1},id2={id2},param={param},p1={p1},p2={p2}"
    print(request.META)
    return HttpResponse(res)


def t_jsonRes(request):
    # data = {"name": "killer", "addr": "shanghai"}
    # JsonResponse 一般只允许放回字典
    # response = JsonResponse(data)
    '''
    对于非字典转换需要设置safe=false,jsonresponse不负责确保安全性
    '''
    data = [
        {
            "name": "rose",
            "addr": "guangzhou"
        },
        {
            "name": "jack",
            "addr": "newyork"
        },
    ]
    response = JsonResponse(data, safe=False)
    return response


def ArticleList(request):
    articles = ArticlePost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)


def ArticleDetails(request, id):
    article = ArticlePost.objects.get(id=id)  #Q:get和filter有什么不同？
    context = {'article': article}
    return render(request, 'article/details.html', context)


def ArticleDelete(request, id):
    if request.method != "POST":
        return HttpResponse("Method Error!!")
    article = ArticlePost.objects.filter(id=id)
    if article.exists():
        article.delete()
    else:
        return HttpResponse("article dose'not error!!")
    return redirect('article:ArticleList')


def ArticleEdit(request, id=None):
    # post请求代表提交数据
    if request.method == 'POST':
        # check data,文章和内容不能为空

        title = request.POST.get("title", "")
        body = request.POST.get("body", "")
        if title == "" or body == "":
            return HttpResponse("title or article can not be empty!!")

        # 如果没有id,那么就是新增
        if id == None:
            article = ArticlePost(
                title=title,
                body=body,
                updated=timezone.now(),
                created=timezone.now(),
                author=User.objects.get(id=1))  #严格来说应该是校验用户的id
            # article.title=request.POST['title'] 也可以用这种写法
            # article.body=request.POST['body']
        # 如果有id,那么就是更新文章
        else:
            if ArticlePost.objects.filter(id=id).exists():
                article = ArticlePost.objects.get(id=id)  #权限校验暂时未作
                article.title = title
                article.body = body
                article.updated = timezone.now()  #需要更新时间
            else:
                return HttpResponse("article dose'not error!!")

        article.save()
        return redirect('article:ArticleList')

    # get方法返回编辑页面
    else:
        context = {}
        # 文章有内容那么返回文章
        if id != None and ArticlePost.objects.filter(id=id).exists():
            article = ArticlePost.objects.get(id=id)
            context = {'article': article}
        return render(request, 'article/edit.html', context)

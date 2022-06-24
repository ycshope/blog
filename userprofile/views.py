from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render

from .forms import UserLoginForm

# Create your views here.


def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        print(f"Post data:{user_login_form}")
        # 直接获取到的是个表单
        #          Post data:<tr><th><label for="id_username">Username:</label></th><td><input type="text" name="username" value="1" required id="id_username"></td></tr>
        # new_blog-web-1  | <tr><th><label for="id_password">Password:</label></th><td><input type="text" name="password" value="1" required id="id_password"></td></tr>
        if user_login_form.is_valid():  #这里会校验能否做序列化
            # 将数据格式化成类似json的东西
            data = user_login_form.cleaned_data
            print(f"data:{data}")
            #  data:{'username': '1', 'password': '1'}

            # 检查数据库中是否有对应的username和password,这里直接用的就是django后台的账号密码
            user = authenticate(username=data['username'],
                                password=data['password'])
            print(f"{user}")
            # 登录失败:None
            # 登录成功:root
            if user:
                login(request, user)
                context = {"user": user}
                return render(request, 'article/list.html', context)
            else:
                return HttpResponse('username or password error!')
        else:
            return HttpResponse('bad forms for username or password !!')
    elif request.method == "GET":
        # 是否生成表格关系不大,因为反正前端也会有form
        # user_login_form = UserLoginForm()
        # context = {'form': user_login_form}
        # return render(request, './login.html', context)
        return render(request, './login.html', {})
    else:
        return HttpResponse('method error!')


def user_logout(request):
    # 退出登录貌似挺简单
    logout(request)
    return redirect('login')


# ref:# https://www.runoob.com/django/django-auth.html
def user_register(request):
    if request.method == "POST":
        # 校验用户的注册信息
        user_login_form = UserLoginForm(data=request.POST)
        print(f"Post data:{user_login_form}")

        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            print("*" * 30)
            print(f"data:{data}")

            #检查是否已经注册
            ret_get = User.objects.filter(username=data['username'])
            if ret_get:
                return HttpResponse('this username already registerd!!')

            ret_reg = User.objects.create_user(username=data['username'],
                                               password=data['password'])
            print(f"ret_reg={ret_reg}")
            
            # 注册成功直接返回到登录页面
            if ret_reg:
                return render(request, 'login.html')
            else:
                return HttpResponse('register error,please try again!!')

        else:
            return HttpResponse('bad form for username or password!!')
    elif request.method == "GET":
        context = {}
        return render(request, 'register.html', context)
    else:
        return HttpResponse('method error!')

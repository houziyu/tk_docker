from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth import authenticate,logout,login
from lib import docker_main

def UserLogin(request):
    #用户登录验证
    errors = {}
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            print('登录完成')
            login(request, user)
            return redirect('/dashboard')
        else:
            print(errors)
            errors = {'error': '用户名或者密码错误，请重新输入'}
            return render(request, 'login.html', errors)

def Dashboard(request):
    #仪表盘
    DockerContainerAll = docker_main.DockerInitial().DockerContainerCictionary()
    print(DockerContainerAll)
    return render(request, 'common/dashboard.html', {'DockerContainerAll': DockerContainerAll})

def UserLogout(request):
    #用户登出
    logout(request)
    return HttpResponseRedirect("/")
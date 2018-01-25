from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from lib import docker_main
from django.contrib.auth.decorators import login_required
from lib import config
from common import models

from django.core.cache import cache
import datetime,os,random,string
from tk_docker import settings
from common import verify
def UserLogin(request):
    #用户登录验证
    errors = {}
    ins_env=config.ins_env
    today_str = datetime.date.today().strftime("%Y%m%d")
    verify_code_img_path = "%s/%s" % (settings.STATICFILES_DIRS[0]+'/verify',
                                      today_str)
    if not os.path.isdir(verify_code_img_path):
        os.makedirs(verify_code_img_path, exist_ok=True)
    print("session:", request.session.session_key)
    # print("session:",request.META.items())
    random_filename = "".join(random.sample(string.ascii_lowercase, 4))
    random_code = verify.gene_code(verify_code_img_path, random_filename)
    cache.set(random_filename, random_code, 30)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        _verify_code = request.POST.get('verify_code')
        _verify_code_key = request.POST.get('verify_code_key')
        print("verify_code_key:", _verify_code_key)
        print("verify_code:", _verify_code)
        if cache.get(_verify_code_key) == _verify_code:
            print("code verification pass!")
            user = authenticate(username=username, password=password)
            if user:
                print('登录完成')
                login(request, user)
                next_url = request.GET.get('next')
                print(next_url)
                if next_url:
                    return redirect(next_url)
                return redirect('/dashboard')
            else:
                errors["error"] = '用户名或者密码错误，请重新输入'
        else:
            errors['error'] = "验证码错误!"
    return render(request, 'login.html', {'ins_env': ins_env, "filename": random_filename, "today_str": today_str,"errors":errors})


@login_required
def Dashboard(request):
    #仪表盘
    host_all = models.host_information.objects.filter(docker_status=1).all()
    if host_all:
        type = request.GET.get('type')
        DockerContainerAll = docker_main.DockerInitial().DockerContainerNow()
        if type:
            DockerContainerAll = sorted(DockerContainerAll, key=lambda k: k[type])
        return render(request, 'common/dashboard.html', {'DockerContainerAll': DockerContainerAll})
    else:
        return HttpResponse('请登录admin添加docker主机信息')

def Computer(request):
    computer_all = models.host_information.objects.all()
    all_computer = []
    for i in computer_all:
        a_computer = {}
        a_computer['host_name'] = i.host_name
        a_computer['host_ip'] = i.host_ip
        a_computer['host_ssh_type'] = i.host_ssh_type
        a_computer['docker_status'] = i.docker_status
        all_computer.append(a_computer)
    print(all_computer)
    return render(request, 'common/computer.html', {'all_computer': all_computer})

def UserLogout(request):
    #用户登出
    logout(request)
    return HttpResponseRedirect("/")
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,logout,login
from lib import docker_main
from django.contrib.auth.decorators import login_required
from lib import config
from common import models
import requests,socket

from django.core.cache import cache
import datetime,os,random,string
from tk_docker import settings
from common import verify
def UserLogin(request):
    #用户登录验证
    errors = {}
    ins_env=config.ins_env
    today_str = datetime.date.today().strftime("%Y%m%d")
    verify_code_img_path = "%s/%s" % (settings.STATICFILES_DIRS[0]+'/verify',today_str)
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

@login_required
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

@login_required
def service_status(request):
    service_status_all = models.service_status_detection.objects.all()
    service_status_list = []
    for i in service_status_all:
        a_servic = {}
        a_servic['id'] = i.id
        a_servic['service_name'] = i.service_name
        a_servic['host_name'] = i.host_name.host_name
        a_servic['url'] = i.url
        a_servic['port'] = i.port
        a_servic['url_status'] = i.url_status
        a_servic['port_status'] = i.port_status
        service_status_list.append(a_servic)
    print(service_status_list)
    return render(request, 'common/service_status.html', {'service_status_list': service_status_list})

def service_status_detection(request):
    service_status_all = models.service_status_detection.objects.all()
    service_return=[]
    for i in service_status_all:
        service_status_dist={}
        url_status = url_detection(i.url)
        port_status = port_detection(i.host_name.host_ip,i.port)
        # 服务状态逻辑。
        return_text=''
        print('url_status:',url_status,'port_status:',port_status)
        if url_status == 200:
            if i.url_status == '1':
                print(i.service_name+':'+'url检测正常。')
            else:
                models.service_status_detection.objects.filter(id=i.id).update(url_status=1)
        else:
            models.service_status_detection.objects.filter(id=i.id).update(url_status=2)
            #并且调用微信通知
            return_text=i.service_name+'服务的url无法访问了.'+'状态码为:'+str(url_status)
        #端口状态逻辑。
        if port_status == '1':
            if i.port_status == '1':
                print(i.service_name+':'+'prot检测正常。')
            else:
                models.service_status_detection.objects.filter(id=i.id).update(port_status='1')
        else:
            models.service_status_detection.objects.filter(id=i.id).update(port_status='2')
            #并且调用微信通知
            return_text=return_text+'---'+i.service_name + '服务的port关闭' + '端口:' + str(i.port)
        service_status_dist[i.service_name]={'url_status':url_status,'port_status':port_status}
        service_return.append(service_status_dist)
        if return_text:
            requests.get('https://pushbear.ftqq.com/sub?sendkey=2638-0cd76e88038120bb0650763efb4566ad&text=clx报警port&desp='+return_text)
    return HttpResponse(service_return)

def url_detection(url):
    if url == 'null':
        http_status= 200
    else:
        html = requests.get(url)  # 用head方法去请求资源头部
        # print(html.status_code)  # 状态码
        http_status = html.status_code

    return http_status

def port_detection(host_ip,port):
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1)
    try:
        sk.connect((host_ip, port))
        sk.close()
        return '1'
    except Exception:
        return '2'

def UserLogout(request):
    #用户登出
    logout(request)
    return HttpResponseRedirect("/")
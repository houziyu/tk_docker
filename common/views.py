from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.http.request import QueryDict
from django.contrib import auth
from django.contrib.auth import logout
from lib import docker_main
from django.contrib.auth.decorators import login_required
from lib import config
from common import models
from script import models as scriptmodels
from django.views.decorators.csrf import csrf_exempt
import requests,socket
import paramiko
import json
from tk_docker import settings
from common import verify
from django.conf import settings  #调用settings
from lib import  mysql_conn
import xlwt
# Create your views here.

def global_setting(request):   #把setting方法读取出来
    return {'SITE_NAME': settings.SITE_NAME,}

def jump(request):
    return HttpResponseRedirect("/login/")

@login_required()
def index(request):
    host_num = models.host_information.objects.all().count()
    DockerContainerNub = len(docker_main.DockerInitial().DockerContainerNow())
    ScriptNum  = scriptmodels.script_data.objects.all().count()
    ServiceErrorNum = models.service_status_detection.objects.filter(url_status=2).filter(port_status=2).count()
    return render(request, 'index.html',{'host_num':host_num,'DockerContainerNub':DockerContainerNub,'ScriptNum':ScriptNum,'ServiceErrorNum':ServiceErrorNum})
    # return render(request, 'index.html',locals())

def UserLogin(request):
    #用户登录验证
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        login_response = {"user": None, "error_msg": ""}
        if request.session.get("verify_code_key") == valid_code:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                login_response["user"] = user.username
            else:
                login_response["error_msg"] = '用户名或者密码错误，请重新输入！！'
        else:
            login_response["error_msg"] = '验证码错误！！请重新输入！！'
        return HttpResponse(json.dumps(login_response))
    else:
        ins_env = config.ins_env
        return render(request, 'login.html', {'ins_env': ins_env, })

def get_valid_img(request):
    data = verify.gene_code(request)
    return HttpResponse(data)

@login_required()
def Dashboard(request):
    #仪表盘
    DockerContainerAll = docker_main.DockerInitial().DockerContainerNow()
    return render(request, 'common/dashboard.html', {'DockerContainerAll': DockerContainerAll})

@login_required()
@csrf_exempt
def Computer(request):
    if request.method == 'GET':
        computer_all = models.host_information.objects.all()
        all_computer = []
        for i in computer_all:
            a_computer = {}
            a_computer['id'] = i.id
            a_computer['host_name'] = i.host_name
            a_computer['host_ip'] = i.host_ip
            a_computer['host_ssh_type'] = i.host_ssh_type
            a_computer['docker_status'] = i.docker_status
            all_computer.append(a_computer)
        print(all_computer)
        return render(request, 'common/computer.html', {'all_computer': all_computer})
    elif request.method == 'POST':
        host_name = request.POST.get('host_name')
        host_ip = request.POST.get('host_ip')
        host_user = request.POST.get('host_user')
        host_ssh_type = request.POST.get('host_ssh_type')
        login_pass = request.POST.get('login_pass')
        login_keyfile = request.POST.get('login_keyfile')
        docker_status = request.POST.get('docker_status')
        print(host_name,host_ip,host_user,host_ssh_type,login_pass,login_keyfile,docker_status)
        try:
            if host_ssh_type == 'password':
                models.host_information.objects.create(host_name=host_name, host_ip=host_ip, host_user=host_user, host_ssh_type=host_ssh_type,
                                               host_password=login_pass,docker_status=docker_status)
            else:
                models.host_information.objects.create(host_name=host_name, host_ip=host_ip, host_user=host_user,host_ssh_type=host_ssh_type,
                                         host_ssh_keyfile_path=login_keyfile, docker_status=docker_status)
        except Exception:
            return HttpResponse("添加失败")
        return HttpResponse("添加成功")
    elif request.method == 'DELETE':
        delete_dict = QueryDict(request.body, encoding='utf-8')
        host_name = delete_dict.get('computer_id')
        print('computer_id:',host_name)
        try:
            models.host_information.objects.filter(id=host_name).delete()
        except Exception:
            return HttpResponse("删除失败")
        return HttpResponse("删除成功")
    # return render(request, 'common/computer.html', locals())

@login_required()
def connection_test(request):
    if request.method == 'POST':
        host_ip = request.POST.get('host_ip')
        host_user = request.POST.get('host_user')
        host_ssh_type = request.POST.get('host_ssh_type')
        login_pass = request.POST.get('login_pass')
        login_keyfile = request.POST.get('login_keyfile')
        print(host_ip,host_user,host_ssh_type,login_pass,login_keyfile)
        try:
            if host_ssh_type== 'keyfile':
                pkey = paramiko.RSAKey.from_private_key_file(login_keyfile)
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=host_ip,
                    port=22,
                    username=host_user,
                    pkey=pkey,
                    timeout=5,)
            elif host_ssh_type == 'password':
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(
                    hostname=host_ip,
                    port=22,
                    username=host_user,
                    password=login_pass,
                    timeout=5,)
        except Exception:
            print('主机添加失败！')
            return HttpResponse("连接失败，请检查相关信息")
        return HttpResponse("连接测试通过")


@login_required()
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

def apitest(request):
    runiter = request.GET.get('runiter')
    all_sql_list=[]
    all_sql = '''select * from testresult order by id desc limit 100;'''
    fail_sql = '''select * from testresult where result=\'fail\' limit 100'''
    if runiter:
        all_sql = '''select * from testresult where runIter=%s'''%(runiter)
        fail_sql = '''select * from testresult where result=\'fail\' and runIter=%s'''%(runiter)
    all_sql_list.append(all_sql)
    all_sql_list.append(fail_sql)
    test_data_all=[]
    for i in all_sql_list:
        results = mysql_conn.test_mysql(i)
        tmp=[]
        for i in results:
            list_format = {'id': i[0], 'method': i[2], 'url': i[3], 'result': i[9], 'comments': i[10],
                           'runIter': i[12]}
            tmp.append(list_format)
        test_data_all.append(tmp)
    return render(request, 'common/apitest.html', {'test_data_all': test_data_all[0],'fail_test_data_all':test_data_all[1]})

def api_details(request):
    apitest_id = request.GET.get('apitest_id')
    sql = '''select * from testresult where id=%s'''%(apitest_id)
    results = mysql_conn.test_mysql(sql)[0]
    print(results)
    test_one_list=[]
    test_one_id = {'title':'id','data':results[0]}
    test_one_caseid = {'title': 'caseid', 'data': results[1]}
    test_one_method = {'title': 'method', 'data': results[2]}
    test_one_url = {'title': 'url', 'data': results[3]}
    test_one_header = {'title': 'header', 'data': results[4]}
    test_one_data = {'title': 'data', 'data': results[5]}
    test_one_response = {'title': 'response', 'data': results[6]}
    test_one_statuscode = {'title': 'statuscode', 'data': results[7]}
    test_one_message = {'title': 'message', 'data': results[8]}
    test_one_result = {'title': 'result', 'data': results[9]}
    test_one_comments = {'title': 'comments', 'data': results[10]}
    test_one_createdTime = {'title': 'createdTime', 'data': results[11]}
    test_one_runIter = {'title': 'runIter', 'data': results[12]}

    test_one_list.append(test_one_id)
    test_one_list.append(test_one_caseid)
    test_one_list.append(test_one_method)
    test_one_list.append(test_one_url)
    test_one_list.append(test_one_header)
    test_one_list.append(test_one_data)
    test_one_list.append(test_one_response)
    test_one_list.append(test_one_statuscode)
    test_one_list.append(test_one_message)
    test_one_list.append(test_one_result)
    test_one_list.append(test_one_comments)
    test_one_list.append(test_one_createdTime)
    test_one_list.append(test_one_runIter)
    return render(request, 'common/apitest_details.html', {'test_one_list': test_one_list})

def api_data_down(request):
    runiter = request.GET.get('runiter')
    file_name = runiter+'.xls'
    fail_sql = '''select * from testresult where result=\'fail\' and runIter=%s''' % (runiter)
    count_fail = '''select count(*) from testresult where result=\'fail\' and runIter=%s''' % (runiter)
    results = mysql_conn.test_mysql(fail_sql)
    count_results = mysql_conn.test_mysql(count_fail)
    wb = xlwt.Workbook(encoding='utf-8')
    sheet = wb.add_sheet("失败数据", cell_overwrite_ok=True)
    sheet.write(0, 0, '%s的失败数据' % runiter)
    sheet.write(1, 0, '总共失败条数')
    sheet.write(1, 1, count_results[0][0])
    sheet.write(2, 0, 'id')
    sheet.write(2, 1, 'caseid')
    sheet.write(2, 2, 'method')
    sheet.write(2, 3, 'url')
    sheet.write(2, 4, 'header')
    sheet.write(2, 5, 'data')
    sheet.write(2, 6, 'response')
    sheet.write(2, 7, 'statuscode')
    sheet.write(2, 8, 'message')
    sheet.write(2, 9, 'result')
    sheet.write(2, 10, 'comments')
    sheet.write(2, 11, 'createdTime')
    sheet.write(2, 12, 'runIter')
    line = 3
    for i in results:
        column = 0
        for y in i:
            print(line, column, y)
            sheet.write(line, column, y)
            column = column + 1
        line = line + 1
    save_path = config.log_dir_master+'/tmp/'+file_name
    wb.save(save_path)
    return render(request, 'log/downandback.html', {'return_results': save_path, 'log_name': file_name})

from django.shortcuts import render,HttpResponse
from . import models
import paramiko
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def Script(request):
    #脚本首页的显示
    ScriptAll = models.script_data.objects.all()
    ScriptAllDictionary=[]
    for i in ScriptAll:
        single = {}
        # for i in ScriptAll:
        parameter=[]
        single['id'] = i.id
        single['script_name']=i.script_name
        single['script_path'] = i.script_path
        single['service_name'] = i.service_name
        single['server_name'] = i.server_name.host_name
        for y in i.script_parameter.values_list():
            parameter.append(y[1])
        parameter = list(reversed(parameter))
        single['parameter'] = parameter
        ScriptAllDictionary.append(single)
    print(ScriptAllDictionary)
    return render(request, 'script/script.html',context={'ScriptAllDictionary':ScriptAllDictionary})

@login_required
def ScriptExecution(request):
    #脚本数据接收执行
    script_id = request.GET.get('script_id')
    script_parameter = request.GET.get('script_parameter')
    script_status = models.script_data.objects.filter(id=script_id).all()[0].status
    if script_status == 1 :
        models.script_data.objects.filter(id=script_id).update(status=2)
        ssh_type = models.script_data.objects.filter(id=script_id).all()[0].server_name.host_ssh_type
        if script_parameter == 'null':
            script_parameter = ''
        host_ip = models.script_data.objects.filter(id=script_id).all()[0].server_name.host_ip
        script_path = models.script_data.objects.filter(id=script_id).all()[0].script_path
        computer_user = models.script_data.objects.filter(id=script_id).all()[0].server_name.host_user
        computer_all = {}
        computer_all['host_ip'] = host_ip
        computer_all['script_path'] = script_path
        computer_all['computer_user'] = computer_user
        computer_all['script_parameter'] = script_parameter
        computer_all['ssh_type'] = ssh_type
        if ssh_type == 'password':
            computer_passw = models.script_data.objects.filter(id=script_id).all()[0].server_name.host_password
            computer_all['computer_passw'] = computer_passw
            print(computer_all)
        elif ssh_type == 'keyfile':
            computer_keyfile = models.script_data.objects.filter(id=script_id).all()[0].server_name.host_ssh_keyfile_path
            computer_all['computer_keyfile'] = computer_keyfile
            print(computer_all)
        else:
            return HttpResponse('查询不到主机ssh连接认证类型')
        result = SshConnect(computer_all)
        result = mark_safe(result)
        models.script_data.objects.filter(id=script_id).update(status=1)
        return render(request, 'script/script_results.html', {'result':result})
    elif script_status == 2 :
        error = '正在编译。请稍后再试。'
        return render(request, 'script/script_results.html', {'error':error})

# def SshConnect(server_name,script_path,script_parameter):
def SshConnect(computer_all):
    command = "bash" + ' ' + computer_all['script_path'] + ' ' + computer_all['script_parameter']
    if computer_all['ssh_type'] == 'keyfile':
        pkey = paramiko.RSAKey.from_private_key_file(computer_all['computer_keyfile'])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(command)
        ssh.connect(
            hostname=computer_all['host_ip'],
            port=22,
            username=computer_all['computer_user'],
            pkey=pkey)
    elif computer_all['ssh_type'] == 'password':
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=computer_all['host_ip'],
            port=22,
            username=computer_all['computer_user'],
            password=computer_all['computer_passw'])
    stdin, stdout, stderr = ssh.exec_command(command)
    out_log_all = stdout.read().decode()
    err_log_all=stderr.read().decode()
    ssh.close()
    if err_log_all:
        return err_log_all
    return   out_log_all
#/Users/yunque/.ssh/id_rsa
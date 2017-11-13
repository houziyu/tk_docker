from django.shortcuts import render,HttpResponse
from  . import models
import paramiko
from django.utils.safestring import mark_safe
from lib import config

# Create your views here.
def Script(request):
    #脚本首页的显示
    ScriptAll = models.script_data.objects.all()
    return render(request, 'script/script.html',context={'ScriptAll':ScriptAll})

def ScriptExecution(request):
    #脚本数据接收执行
    script_id = request.GET.get('script_id')
    script_parameter = request.GET.get('script_parameter')
    script_status = models.script_data.objects.filter(id=script_id).all()[0].status
    if script_status == 1 :
        models.script_data.objects.filter(id=script_id).update(status=2)
        if script_parameter == 'null':
            script_parameter = ''
        server_name = models.script_data.objects.filter(id=script_id).all()[0].server_name
        script_path = models.script_data.objects.filter(id=script_id).all()[0].script_path
        result = SshConnect(server_name,script_path,script_parameter)
        result = mark_safe(result)
        models.script_data.objects.filter(id=script_id).update(status=1)
        return render(request, 'script/script_results.html', {'result':result})
    elif script_status == 2 :
        error = '正在编译。请稍后再试。'
        return render(request, 'script/script_results.html', {'error':error})

def SshConnect(server_name,script_path,script_parameter):
    pkey = paramiko.RSAKey.from_private_key_file(config.key_address)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    command = "bash" + ' ' +script_path + ' ' + script_parameter
    print(command)
    ssh.connect(
                hostname=server_name,
                port=22,
                username='root',
                pkey=pkey)
    stdin, stdout, stderr = ssh.exec_command(command)
    out_log_all = stdout.read().decode()
    err_log_all=stderr.read().decode()
    ssh.close()
    if err_log_all:
        return err_log_all
    return   out_log_all
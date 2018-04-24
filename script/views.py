from django.shortcuts import render,HttpResponse
from . import models
import paramiko
from dwebsocket.decorators import accept_websocket
from django.contrib.auth.decorators import login_required
import threading,datetime
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
        single['service_name'] = i.service_name
        single['server_name'] = i.server_name.host_name
        single['last_execution'] = i.last_execution
        for y in i.script_parameter.values_list():
            parameter.append(y[1])
        parameter = list(reversed(parameter))
        single['parameter'] = parameter
        ScriptAllDictionary.append(single)
    print(ScriptAllDictionary)
    return render(request, 'script/script.html',context={'ScriptAllDictionary':ScriptAllDictionary})

@login_required
def script_results(request):
    script_id = request.GET.get('script_id')
    script_parameter = request.GET.get('script_parameter')
    script_status = models.script_data.objects.filter(id=script_id).all()[0].status
    if script_status == 1:
        script_info = {}
        script_info['script_id'] = script_id
        script_info['script_parameter'] = script_parameter
        now_time = datetime.datetime.now()
        models.script_data.objects.filter(id=script_id).update(last_execution=now_time)
        return render(request, 'script/script_results.html',{'script_info':script_info})
    elif script_status == 2:
        error = '正在编译。请稍后再试。'
        return render(request, 'script/script_results.html', {'error': error})

@accept_websocket
def ScriptExecution(request):
    if request.is_websocket():  # 判断是不是websocket连接
        for i in request.websocket:
            if i is None:
                break
            script_info = eval(i.decode('utf-8'))
            print(script_info)
            script_id  = script_info['script_id']
            script_parameter = script_info['script_parameter']
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
            SshConnect(computer_all,request.websocket)
            models.script_data.objects.filter(id=script_id).update(status=1)
            print('脚本状态更变为1')

def line_buffered(f):
    while not f.channel.exit_status_ready():
        line_buf = f.readline()
        yield line_buf

# def SshConnect(server_name,script_path,script_parameter):
def SshConnect(computer_all,socket):
    command = "bash" + ' ' + computer_all['script_path'] + ' ' + computer_all['script_parameter']
    print('command:',command)
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
    thread_1 = threading.Thread(target=aaa,args=(stdout,socket,))  # 实例化一个线程对象，使线程执行这个函数
    thread_2 = threading.Thread(target=aaa,args=(stderr,socket,))  # 实例化一个线程对象，使线程执行这个函数
    thread_1.start()
    thread_2.start()
    thread_1.join()
    thread_2.join()
    script_complete = '脚本执行完成'
    script_complete = bytes(script_complete, encoding='utf-8')
    socket.send(script_complete)
    ssh.close()

def aaa(log,socket):
    for i in line_buffered(log):
        socket.send(i.encode())
        print(i.encode())
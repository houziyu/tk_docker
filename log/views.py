from django.shortcuts import render,HttpResponse
from django.http import StreamingHttpResponse
from lib import docker_main
from lib import config
import datetime,time
import os,zipfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from collections import deque
from dwebsocket.decorators import accept_websocket
# Create your views here.
@login_required
def LogNow(request):
    # 接收前端传递参数进行计算返回渲染后的页面
    if request.method == 'GET':
        Hostname = request.GET.get('hostname')
        ContainerName = request.GET.get('container_name')
        log_type = request.GET.get('log_type')
        if log_type == 'log_info':
            logs = DockerLog(Hostname, ContainerName)
            info = {'logs':logs,'log_type':log_type ,'hostname': Hostname, 'container_name': ContainerName}
            return render(request, 'log/lognow.html', info)
            # 获取到了容器的name 然后去lib中搜索name的容器然后进行日志打印
        elif log_type == 'log_error':
            docker_download_log_path = DockerUpdateALog(Hostname, ContainerName, log_type)
            f = open(docker_download_log_path['return_results'])
            log_format = f.readlines()
            log_format = deque(log_format, 500)
            log_all = ''
            for i in log_format:
                log_all = log_all + i
            info = {'logs': log_all,'log_type':log_type , 'hostname': Hostname, 'container_name': ContainerName}
            return render(request, 'log/lognow.html', info)

def DockerLog(Hostname, ContainerName):
    # 调取所有容器判断健康度，然后返回日志.
    DockerContainerAll = docker_main.DockerInitial().DockerContainerCictionary()
    ContainerAll = DockerContainerAll[Hostname]
    for i in ContainerAll:
        if ContainerName in i.name:
            b_logs = i.logs(tail=config.log_tail_line)
            return b_logs

@accept_websocket
def log_socket(request):
    if request.is_websocket():  # 判断是不是websocket连接
        for i in request.websocket:
            if i is None:
                break
            print(i)
            log_info =eval(i.decode('utf-8'))
            print(log_info)
            hostname = log_info['hostname']
            container_name = log_info['container_name']
            DockerContainerAll = docker_main.DockerInitial().DockerContainerCictionary()
            ContainerAll = DockerContainerAll[hostname]
            for i in ContainerAll:
                if container_name in i.name:
                    for line in i.logs(tail=0,stream=True):
                        request.websocket.send(line)

@login_required
def LogDump(request):
    # 当天日志的下载以及全部的日志备份
    if request.method == 'GET':
        all_log = request.GET.get('all_log')
        hostname = request.GET.get('hostname')
        container_name = request.GET.get('container_name')
        log_type = request.GET.get('log_type')
        if all_log:
            try:
                docker_log_bak = DockerUpdateAllLog()
                return HttpResponse(docker_log_bak)
            except Exception:
                return HttpResponse('备份出错！')
        elif hostname and container_name and log_type:
            print(hostname,container_name)
            docker_download_log_path = DockerUpdateALog(hostname=hostname,container_name=container_name,log_type=log_type)
            print(docker_download_log_path)
            return render(request, 'log/downandback.html', docker_download_log_path)

#docker log的备份，分两种方式，一种是所有的日志全部备份在升级前，第二种是开发人员查看当天的日志需要进行下拉下载操作临时文件都保存在了tmp目录下
def DockerUpdateAllLog():
    # 全部日志备份
    docker_container_all = docker_main.DockerInitial().DockerContainerCictionary()
    for i in docker_container_all:
        for y in docker_container_all[i]:
            service_name = y.name.split('-')[0]
            if y.status == 'running':
                if service_name in config.service_name_list:
                    service_name = service_name + '-service'
                    log_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    service_log_path = '/logs/' + service_name + '/log_info.log'
                    log_init = y.get_archive(service_log_path)
                    # log_str = b''.join(chunk for chunk in log_init[0]).decode('utf-8')
                    log_str = str(log_init[0].data, encoding="utf-8")
                    # log_str = ''
                    # for i in log_init[0]:
                    #     log_str = log_str + str(i, encoding="utf-8")
                    log_dir_master = config.log_dir_master
                    log_local_name = log_dir_master +'/'+ service_name + '/update/'+'update'+ i + '-' + service_name + '-' + log_date + '.log'
                    log_file = open(log_local_name, 'a+')
                    date_now = str(datetime.datetime.now())
                    log_file.write('执行时间:' + date_now)
                    log_file.write(log_str)
                    log_file.close()
    return_results = '备份成功！！'
    return return_results

def DockerUpdateALog(hostname,container_name,log_type):
    # 某个容器的日志下载
    docker_container_all = docker_main.DockerInitial().DockerContainerCictionary()
    for i in docker_container_all[hostname]:
        if container_name in i.name :
            service_name = i.name.split('-')[0]
            service_name = service_name + '-service'
            if i.status == 'running':
                log_date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                print(log_date,service_name,log_type)
                service_log_path = '/logs/' + service_name + '/'+log_type+'.log'
                print('/logs/' + service_name + '/'+log_type+'.log')
                log_init = i.get_archive(service_log_path)
                # log_all = b''.join(chunk for chunk in log_init[0]).decode('utf-8')
                # log_all = str(log_init[0].data, encoding="utf-8")
                # log_all= ''
                # for i in log_init[0]:
                #     log_all = log_all +  str(i, encoding="utf-8")
                log_name = hostname + '-' + service_name + '-' + log_date + '-' +  log_type + '.log'
                log_dir_master = config.log_dir_master
                log_path = log_dir_master + '/'+'tmp/' + log_name
                date_now = str(datetime.datetime.now())
                date_now = bytes(date_now, encoding="utf8")
                with open(log_path,'wb') as fd:
                    fd.write(date_now)
                    for chunk in log_init[0]:
                        fd.write(chunk)
                    print('bak ok ~!')
                # log_file = open(log_path, 'a+')
                # log_file.write('执行时间:' + date_now+'\n')
                # log_file.write(log_all)
                # log_file.close()
                return_results = {'return_results': log_path, 'log_name': log_name}
                return return_results
            else:
                return_results = {'return_results': None, 'log_name': 'docker容器状态为exit，请检查！'}
                return return_results

@login_required
def LogDownload(request):
    if request.method == 'GET':
        log_path = request.GET.get('log_path')
        log_name = request.GET.get('log_name')
        print('log_path:', log_path, 'log_name:', log_name)
        # 定义zip文件名称。
        zip_file_name = log_name + '.zip'
        # 打包文件后置放的目录地址。
        zip_dir = config.log_dir_master + '/' + 'tmp/' + zip_file_name
        archive = zipfile.ZipFile(zip_dir, 'w', zipfile.ZIP_DEFLATED)
        # 写入zip中文件的地址及名称
        archive.write(log_path)
        # 写入结束
        archive.close()
        print(zip_dir)
        if os.path.isfile(zip_dir):
            response = StreamingHttpResponse(readFile(zip_dir))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(zip_file_name)
            return response
        else:
            return HttpResponse('没有这个文件')

def readFile(filename, chunk_size=512):
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

@login_required
def LogDir(request):
    if request.method == 'GET':
        log_list = config.service_name_list
        service_name_all = []
        for i in log_list:
            y = i + '-service'
            service_name_all.append(y)
        print(service_name_all)
        return render(request, 'log/logdir.html', {'service_now': service_name_all})

@login_required
def LogDirList(request):
    service_name = request.GET.get('service_name')
    log_type = request.GET.get('log_type')
    print(service_name, log_type)
    log_path = config.log_dir_master
    service_name_path = log_path + '/' + service_name + '/' + log_type
    all_file = []
    for i in os.listdir(service_name_path):
        file_path = service_name_path + '/' + i
        if os.path.isfile(file_path):
            file_create_time = os.path.getctime(file_path)
            time_struct = time.localtime(file_create_time)
            time_24 = time.strftime('%Y-%m-%d %H:%M:%S', time_struct)
            all_file.append([i, file_path,time_24])
    print('all_file:',all_file)
    return render(request, 'log/catdownlog.html', {'all_file': all_file,'service_name':service_name,'log_type':log_type})
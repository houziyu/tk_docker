from django.shortcuts import render,HttpResponse
from django.http import StreamingHttpResponse
from lib import docker_main
from lib import config
from django.utils.safestring import mark_safe
import datetime
import os,zipfile
# Create your views here.
def LogNow(request):
    # 接收前端传递参数进行计算返回渲染后的页面
    if request.method == 'GET':
        FindTime = ''
        Hostname = request.GET.get('hostname')
        ContainerName = request.GET.get('container_name')
        if request.GET.get('find_time'):
            FindTime = request.GET.get('find_time')
        logs = DockerLog(Hostname, ContainerName, FindTime)
        logs_str = mark_safe(str(logs, encoding="utf-8"))
        info = {'logs': logs_str, 'hostname': Hostname, 'container_name': ContainerName}
        return render(request, 'log/lognow.html', info)
        # 获取到了容器的name 然后去lib中搜索name的容器然后进行日志打印
    return HttpResponse('ok')

def DockerLog(Hostname, ContainerName, FindTime):
    # 调取所有容器判断健康度，然后返回日志.
    DockerContainerAll = docker_main.DockerInitial().DockerContainerCictionary()
    ContainerAll = DockerContainerAll[Hostname]
    for i in ContainerAll:
        if i.name == ContainerName:
            if i.status == 'running':
                if FindTime:
                    FindTime = int(FindTime)
                    DatetimeNow = datetime.datetime.now() + datetime.timedelta(minutes=-FindTime)
                    print(DatetimeNow)
                    b_logs = i.logs(since=DatetimeNow)
                    return b_logs
                else:
                    b_logs = i.logs(tail=config.log_tail_line)
                    return b_logs
            else:
                results_all = bytes('此容器状态为exited,请检查', encoding="utf8")
                return results_all

def LogDump(request):
    # 当天日志的下载以及全部的日志备份
    if request.method == 'GET':
        all_log = request.GET.get('all_log')
        hostname = request.GET.get('hostname')
        container_name = request.GET.get('container_name')
        if all_log:
            docker_log_bak = DockerUpdateAllLog()
            return render(request, 'log/downandback.html', docker_log_bak)
        elif hostname and container_name:
            docker_download_log_path = DockerUpdateALog(hostname=hostname,container_name=container_name)
            return render(request, 'log/downandback.html', docker_download_log_path)
        else:
            errors = {'return_results': '参数传递有错误！请检查!', 'log_name': None}
            return render(request, 'log/downandback.html', errors)
    return HttpResponse('出错了~')

#docker log的备份，分两种方式，一种是所有的日志全部备份在升级前，第二种是开发人员查看当天的日志需要进行下拉下载操作临时文件都保存在了tmp目录下
def DockerUpdateAllLog():
    # 全部日志备份
    docker_container_all = docker_main.DockerInitial().DockerContainerCictionary()
    for i in docker_container_all:
        for y in docker_container_all[i]:
            service_name = y.name.split('-')[0]
            if y.status == 'running':
                if service_name in config.service_name_list:
                    log_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    service_log_path = '/logs/' + service_name + '-service/log_info.log'
                    log_init = y.get_archive(service_log_path)
                    log_str = str(log_init[0].data, encoding="utf-8")
                    log_dir_master = config.log_dir_master
                    log_local_name = log_dir_master +'/'+ service_name+'-service' + '/update/'+'update'+ i + '-' + service_name + '-' + log_date + '.log'
                    log_file = open(log_local_name, 'a+')
                    date_now = str(datetime.datetime.now())
                    log_file.write('执行时间:' + date_now)
                    log_file.write(log_str)
                    log_file.close()
    return_results = {'return_results': '!备份成功!返回主页!', 'log_name': None}
    return return_results

def DockerUpdateALog(hostname,container_name):
    # 某个容器的日志下载
    docker_container_all = docker_main.DockerInitial().DockerContainerCictionary()
    docker_container_list = docker_container_all[hostname]
    for i in docker_container_list:
        if i.name == container_name:
            service_name = i.name.split('-')[0]
            if i.status == 'running':
                if service_name in config.service_name_list:
                    log_date = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
                    service_log_path = '/logs/' + service_name + '-service/log_info.log'
                    log_init = i.get_archive(service_log_path)
                    log_str = str(log_init[0].data, encoding="utf-8")
                    log_name = hostname + '-' + service_name + '-' + log_date + '.log'
                    log_dir_master = config.service_name_list
                    log_local_name = log_dir_master + '/'+'tmp/' + log_name
                    print(log_local_name)
                    log_file = open(log_local_name, 'a+')
                    date_now = str(datetime.datetime.now())
                    log_file.write('执行时间:' + date_now)
                    log_file.write(log_str)
                    log_file.close()
                    return_results = {'return_results': log_local_name, 'log_name': log_name}
                    return return_results
            else:
                return_results = {'return_results': None, 'log_name': 'docker容器状态为exit，请检查！'}
                return return_results

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

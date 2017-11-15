from django.test import TestCase

# Create your tests here.
import datetime
from lib import config


import docker
from lib import config
import datetime

class DockerInitial(object):
    #docker连接初始化操作
    def __init__(self):
        host_list = config.host_list
        self.docker_all = {}
        for i in host_list:
            self.docker_singleton = docker.DockerClient(base_url='tcp://%s:2375'%i)
            self.docker_all[i] = self.docker_singleton
        print('docker_host_dictionary:',self.docker_all)
    #docker调用所有容器，做成列表交给别的方法进行处理
    def DockerContainerCictionary(self):
        docker_container_all = {}
        for i,v in self.docker_all.items():
            docker_container_all[i]= v.containers.list(all=True)
        print('docker_container_all:',docker_container_all)
        return docker_container_all


#定时下拉备份日志 python3 manage.py crontab add  启动后记得添加上定时任务(python3 manage.py crontab remove)删除
def cron_dump_log():
    docker_container_all = DockerInitial().DockerContainerCictionary()
    for i in docker_container_all:
        hostname= i
        for y in docker_container_all[i]:
            service_name = y.name.split('-')[0]
            if y.status == 'running':
                print(service_name)
                log_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
                num = 0
                try:
                    while True:
                        service_log_path = '/logs/' + service_name + '-service' + '/info/log-info-' + log_date + '.' + str(num) + '.log'
                        log_init = y.get_archive(service_log_path)
                        log_str = str(log_init[0].data, encoding="utf-8")
                        log_local_name = config.log_dir_master+ '/' + service_name + '-service/' + hostname + '-' + service_name + '-' + log_date + '.' + str(num) + '.log'
                        print(log_local_name)
                        log_file = open(log_local_name, 'a+')
                        log_file.write('执行时间:' + log_date)
                        log_file.write(log_str)
                        log_file.close()
                        num += 1
                except BaseException:
                    pass


cron_dump_log()
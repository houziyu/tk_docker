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


    #docker log的备份，分两种方式，一种是所有的日志全部备份在升级前，第二种是开发人员查看当天的日志需要进行下拉下载操作临时文件都保存在了tmp目录下
    def docker_update_log(self,all_log=None,hostname=None,container_name=None):
        if all_log:
            print('这里是全员备份')
            docker_container_all = docker_initial().docker_container_dictionary()
            for i in docker_container_all:
                hostname = i
                for y in docker_container_all[i]:
                    service_name = y.name.split('-')[0]
                    if y.status == 'running':
                        if service_name in config.service_name_list:
                            log_date = (datetime.datetime.now() + datetime.timedelta(hours=+8)).strftime("%Y-%m-%d")
                            service_log_path = '/logs/' + service_name + '-service/log_info.log'
                            log_init = y.get_archive(service_log_path)
                            log_str = str(log_init[0].data, encoding="utf-8")
                            log_dir_master = config.log_dir_master
                            log_local_name = log_dir_master + service_name + '-service/update/'+'update'+ hostname + '-' + service_name + '-service' + '-' + log_date + '.log'
                            log_file = open(log_local_name, 'a+')
                            date_now = str(datetime.datetime.now())
                            log_file.write('执行时间:' + date_now)
                            log_file.write(log_str)
                            log_file.close()
            return_results = {'return_results': '!备份成功!返回主页!', 'log_name': None}
            return return_results
        elif hostname and container_name:
            print('别跑错地方了')
            docker_container_all = docker_initial().docker_container_dictionary()
            docker_container_list = docker_container_all[hostname]
            print(docker_container_list)
            for i in docker_container_list:
                if i.name == container_name:
                    service_name = i.name.split('-')[0]
                    if i.status == 'running':
                        if service_name in config.service_name_list:
                            log_date = (datetime.datetime.now() + datetime.timedelta(hours=+8)).strftime("%Y-%m-%d-%H:%M:%S")
                            service_log_path = '/logs/' + service_name + '-service/log_info.log'
                            print(service_name,log_date,service_log_path)
                            log_init = i.get_archive(service_log_path)
                            log_str = str(log_init[0].data, encoding="utf-8")
                            log_name = hostname + '-' +service_name +'-'+ log_date + '.log'
                            log_dir_master = config.log_dir_master
                            log_local_name = log_dir_master +'tmp/' + log_name
                            print(log_local_name)
                            log_file = open(log_local_name, 'a+')
                            date_now = str(datetime.datetime.now())
                            log_file.write('执行时间:' + date_now)
                            log_file.write(log_str)
                            log_file.close()
                            return_results = {'return_results': log_local_name,'log_name':log_name}
                            return return_results
                    else:
                        return_results = {'return_results': None, 'log_name': 'docker容器状态为exit，请检查！'}
                        return return_results
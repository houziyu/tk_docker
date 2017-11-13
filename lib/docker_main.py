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
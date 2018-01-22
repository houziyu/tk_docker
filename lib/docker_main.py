import docker
from lib import config
import traceback
from common import models

class DockerInitial(object):
    #docker连接初始化操作
    def __init__(self):
        hostall = models.host_information.objects.filter(docker_status=1).all()
        self.docker_all = {}
        for i in hostall:
                self.docker_singleton = docker.DockerClient(base_url='tcp://%s:2375' % i.host_ip)
                self.docker_all[i.host_name] = self.docker_singleton
        print('docker_host_dictionary:',self.docker_all)
    #docker调用所有容器，做成列表交给别的方法进行处理
    def DockerContainerCictionary(self):
        docker_container_all = {}
        for i,v in self.docker_all.items():
            docker_container_all[i]= v.containers.list(all=True)
        print('docker_container_all:',docker_container_all)
        return docker_container_all

    def DockerContainerNow(self):
        DockerContainerObject = {}
        for i, v in self.docker_all.items():
            DockerContainerObject[i] = v.containers.list(all=True)
        DockerContainerAllList = []
        for i in DockerContainerObject:
            hostname = i
            for y in DockerContainerObject[i]:
                data = {}
                data['hostname'] = hostname
                data['name'] = y.name
                data['image'] = y.image.tags[0]
                data['short_id'] = y.short_id
                data['status'] = y.status
                print(data)
                DockerContainerAllList.append(data)
        return DockerContainerAllList
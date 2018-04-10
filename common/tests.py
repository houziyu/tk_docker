from django.test import TestCase

# Create your tests here.
from tk_docker import settings
import docker
docker_singleton = docker.DockerClient(base_url='tcp://192.168.1.60:2375')
log_liu = docker_singleton.containers.list(all=True)[0].logs(stream=True,tail=200)
for i in log_liu:
    print(i)
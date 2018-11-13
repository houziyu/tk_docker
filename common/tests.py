import docker
# Create your tests here.

# docker_singleton = docker.DockerClient(base_url='tcp://192.168.1.60:2375')

# aa = docker_singleton.containers.list(all=True)
# for i in aa:
    # if i.name == 'payment-service-8301':
        # for line in i.logs(tail=5,stream=True):
#         #    print(dir(i.logs(tail=5,stream=True)))
#
#
# dmmmvmnf = _url('/containers/{0}/archive', 'aaa')
# print(dmmmvmnf)
# base_url='tcp://16892.168.1.60:2375'
# # aa = base_url.strip()
# # print(aa)
def login(func):
    def inner(*args,**kwargs):
        ret = func(*args,**kwargs)
        print('aaa')
        return ret
    return inner

@login
def aaa(a):
    print(a)

aaa('hghggg')
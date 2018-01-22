from django.db import models

# Create your models here.

class host_information(models.Model):
    #脚本的具体参数信息
    host_name = models.CharField(max_length=40)
    host_ip = models.GenericIPAddressField(max_length=40)
    host_ssh_type = models.CharField(max_length=40,choices=[('password', '密码登录'),('keyfile', '密钥登录'),],default=1)
    host_ssh_keyfile_path = models.CharField(blank=True,max_length=100)
    host_user = models.CharField(max_length=40)
    host_password = models.CharField(max_length=40,blank=True)
    #主机增加一个字段来指定服务器是否使用docker，因为会出现添加一个主机只使用脚本功能不使用docker功能
    docker_status = models.CharField(max_length=40,choices=[('1', '使用'),('2', '不使用'),],default=2)
    def __str__(self):
        return self.host_name
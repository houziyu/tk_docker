from django.db import models
from common.models import host_information

# Create your models here.

class all_parameter(models.Model):
    #脚本的参数
    parameter = models.CharField(max_length=20)
    def __str__(self):
        return self.parameter

class script_data(models.Model):
    #脚本的具体参数信息
    script_name = models.CharField(max_length=40)
    script_path = models.CharField(max_length=100)
    service_name = models.CharField(max_length=40)
    server_name = models.ForeignKey(host_information,on_delete=models.CASCADE,)
    script_parameter = models.ManyToManyField(all_parameter,blank=True)
    status = models.IntegerField(choices=[(1, '空闲中'),(2, '进行中'),],default=1)
    last_execution = models.CharField(max_length=50,blank=True)
    def __str__(self):
        return self.script_name
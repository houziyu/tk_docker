from lib.docker_main import DockerInitial
import datetime
from lib import config
import requests

#定时下拉备份日志 python3 manage.py crontab add  启动后记得添加上定时任务(python3 manage.py crontab remove)删除
#备份info日志
def cron_dump_info_log():
    docker_container_all = DockerInitial().DockerContainerCictionary()
    for i in docker_container_all:
        hostname= i
        for y in docker_container_all[i]:
            service_name = y.name.split('-')[0]
            if y.status == 'running':
                log_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
                num = 0
                try:
                    while True:
                        log_type='info'
                        service_log_path = '/logs/' + service_name + '-service' + '/'+log_type+'/log-'+log_type+'-' + log_date + '.' + str(num) + '.log'
                        log_init = y.get_archive(service_log_path)
                        log_str = str(log_init[0].data, encoding="utf-8")
                        log_local_name = config.log_dir_master+ '/' + service_name + '-service/' + log_type +'/'+ hostname + '-' + service_name +'-'+ log_type +'-' + log_date + '.' + str(num) + '.log'
                        print(service_log_path)
                        print(log_local_name)
                        log_file = open(log_local_name, 'a+')
                        log_file.write('执行时间:' + log_date)
                        log_file.write(log_str)
                        log_file.close()
                        num += 1
                except BaseException:
                    pass

#备份error日志
def cron_dump_error_log():
    docker_container_all = DockerInitial().DockerContainerCictionary()
    for i in docker_container_all:
        hostname= i
        for y in docker_container_all[i]:
            service_name = y.name.split('-')[0]
            if y.status == 'running':
                log_date = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
                num = 0
                try:
                    while True:
                        log_type='error'
                        service_log_path = '/logs/' + service_name + '-service' + '/'+log_type+'/log-'+log_type+'-' + log_date + '.' + str(num) + '.log'
                        log_init = y.get_archive(service_log_path)
                        log_str = str(log_init[0].data, encoding="utf-8")
                        log_local_name = config.log_dir_master+ '/' + service_name + '-service/' + log_type +'/'+ hostname + '-' + service_name +'-'+ log_type +'-' + log_date + '.' + str(num) + '.log'
                        print(service_log_path)
                        print(log_local_name)
                        log_file = open(log_local_name, 'a+')
                        log_file.write('执行时间:' + log_date)
                        log_file.write(log_str)
                        log_file.close()
                        num += 1
                except BaseException:
                    pass

#定时检查服务运行情况
def check_service():
    requests.get('http://127.0.0.1:8080/service_status_detection/')
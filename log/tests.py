from django.test import TestCase
from lib.docker_main import DockerInitial
import datetime
from lib import config

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

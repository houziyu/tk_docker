#tk_docker
1.老铁star点一点走一走,以前项目叫dao_manage太俗该改名了。所以叫tk_docker。此项目使用的是python3.6暂未测试过python2系列<br>
2.现在这个项目在本公司生产环境跑，可以说非常稳定了。但是如果大家使用的话需要看下`/tk_docker/log/cron_dump_log.py`中以及`/tk_docker/common/views`中的代码有的地方因为业务关系我给写死了。叉会腰~<br>
---
3.长啥样？看图<br>
![](https://github.com/houziyu/tk_docker/raw/master/document/img/login.png)
![](https://github.com/houziyu/tk_docker/raw/master/document/img/index.png)
![](https://github.com/houziyu/tk_docker/raw/master/document/img/log.png)
![](https://github.com/houziyu/tk_docker/raw/master/document/img/computer.png)
![](https://github.com/houziyu/tk_docker/raw/master/document/img/history_log.png)
![](https://github.com/houziyu/tk_docker/raw/master/document/img/service_status.png)
---
4.`pip install -r requirements.txt`<br>
5.`python manage.py makemigrations`和`python manage.py migrate` 如果出现报错请删除`db.sqlite3`文件<br>
6.`python manage.py python manage.py create superuser`创建一个用户，把`/tk_docker/tk_docker/settings.py`中的一个参数改一下`DEBUG=True`<br>
7.如果此时去访问`127.0.0.1:8000`登录的话会告诉你去登录admin添加doker主机信息。然后访问`127.0.0.1:8000/admin`中的`host_informations`添加一条主机数据<br>
8.只要填写相应的信息即可，如果不需要使用脚本功能的话可以不写密码或者密钥路径。效果如图下:<br>
![](https://github.com/houziyu/tk_docker/raw/master/document/img/manage.png)
9.在脚本`seript_datas`中添加脚本信息的时候是关联到主机属于一对多类型。但是脚本虽然可以增加执行参数，但是只支持一个参数。如果有需求二次开发吧。<br>
10.log日志info查看是根据`docker api`进行调取日志的。但是error是根据文件，从容器中下载error文件打开返回文本。不是通过api注意这点~<br>
11.`/tk_docker/lib/config.py`中的参数`log_tail_line`是查看容器info日志默认输出多少行。`service_name_list`在仪表盘时候显示筛选服务，具体实现方法请看代码。`log_dir_master`日志每日备份保存地址。`ins_env`登录界面上面显示的环境说明<br>
12.还有需要一点注意的是`/tk_docker/log/cron_dump_log.py`中的代码自己改~。`django-crontab`这模块怎么应用去百度一下就好。很简单。<br>
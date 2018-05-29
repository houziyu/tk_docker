"""tk_docker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^log/now/$', views.LogNow, name='lognow'),
    url(r'^log/dump/$', views.LogDump, name='logdump'),
    url(r'^log/download/$', views.LogDownload, name='logdownload'),
    url(r'^log/dir/$', views.LogDir, name='logdir'),
    url(r'^log/dir/page/$', views.LogDirPage, name='logdirpage'),
    url(r'^log/log_socket/$', views.log_socket, name='log_socket'),
]

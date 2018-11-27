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
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.jump,),
    url(r'^index/$', views.index,name='index'),
    url(r'^login/$', views.UserLogin, name='login'),
    url(r'^dashboard/$', views.Dashboard, name='dashboard'),
    url(r'^get_valid_img/$', views.get_valid_img, name='get_valid_img'),
    url(r'^log_out/$', views.UserLogout, name='logout'),
    url(r'^computer/$', views.Computer, name='computer'),
    url(r'^connection_test/$', views.connection_test, name='connection_test'),
    url(r'^service_status/$', views.service_status, name='service_status'),
    url(r'^service_status_detection/$', views.service_status_detection, name='service_status_detection'),
    url(r'^apitest/$', views.apitest, name='apitest'),
    url(r'^apitest/details/$', views.api_details, name='api_details'),
    url(r'^apitest/down/$', views.api_data_down, name='api_data_down'),
]

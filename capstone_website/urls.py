"""capstone_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from health.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index),
    path('illness/', illness),
    path('update/', update_diagram),
    path('summary/', get_summary),
    path('tweets/', list_tweets),
    path('cfg/tweets/', labelled_tweets),
    path('cfg/get_cfg_tweets/', get_labelled_tweets),
    path('cfg/dictionary/', dictionary),
]

"""
URL configuration for Lingxi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from .controller import welcomecontroller as wel
from .controller import studentcontroller as stu
from .controller import chatapi as ca

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", wel.welcome),
    path("index/", wel.welcome),
    path("findstudents/", stu.findstudent),
    path("chat/", ca.getchat),
    path('appp/', include('users.urls')),
]

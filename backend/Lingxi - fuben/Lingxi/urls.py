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
from .controller import diary_generator as diary
from .controller import tts_service as tts

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", wel.welcome),
    path("index/", wel.welcome),
    path("findstudents/", stu.findstudent),    path("chat/", ca.getchat),  # 原有的聊天API
    path("enhanced-chat/", ca.enhanced_chat),  # 新的增强聊天API
    path("chat-history/", ca.get_chat_history),  # 获取聊天历史
    
    # 情绪日记相关API
    path("generate-diary/", diary.generate_emotion_diary),  # 生成情绪日记
    path("get-diary/", diary.get_emotion_diary),  # 获取指定日期的日记
    path("diary-dates/", diary.get_diary_dates),  # 获取有日记的日期列表
    path("emotion-trend/", diary.get_emotion_trend),  # 获取情绪趋势数据
    path("delete-diary/", diary.delete_emotion_diary),  # 删除指定日期的日记
    
    # TTS语音服务相关API
    path("nahida-tts/", tts.nahida_tts),  # Nahida TTS语音合成
    path("tts-status/", tts.check_tts_status),  # 检查TTS服务状态
    
    path('appp/', include('users.urls')),
]

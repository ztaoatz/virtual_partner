# users/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # 原有路由
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    
    # 新增邮件验证相关路由
    path('send-verification-code/', views.send_verification_code, name='send_verification_code'),
    path('verify-email-code/', views.verify_email_code, name='verify_email_code'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
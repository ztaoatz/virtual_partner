from django.shortcuts import render

# Create your views here.
# users/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
import json
import uuid

@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('phoneNumber')
        password = data.get('password')
        if username and password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'message': '用户已存在'})
            
            # 创建用户
            user = User.objects.create_user(username=username, password=password)
            
            # 创建用户资料
            external_user_id = str(uuid.uuid4())
            profile = UserProfile.objects.create(
                user=user,
                nickname=username,
                external_user_id=external_user_id
            )
            
            return JsonResponse({
                'success': True, 
                'message': '注册成功',
                'user_id': external_user_id,
                'username': username
            })
        return JsonResponse({'success': False, 'message': '缺少账号或密码'})
    return JsonResponse({'success': False, 'message': '无效请求'})



@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            django_login(request, user)
            
            # 获取或创建用户资料
            try:
                profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                # 如果没有资料，创建一个
                external_user_id = str(uuid.uuid4())
                profile = UserProfile.objects.create(
                    user=user,
                    nickname=user.username,
                    external_user_id=external_user_id
                )
            
            menu_list = [
                {
                    "id": 1,
                    "name": "用户管理",
                    "path": "/user",
                },
                {
                    "id": 2,
                    "name": "商品管理",
                    "path": "/goods",
                },
                {
                    "id": 3,
                    "name": "订单管理",
                    "path": "/order",
                }
            ]
            return JsonResponse({
                'success': True, 
                'menuList': menu_list, 
                'message': '登录成功',
                'user_id': profile.external_user_id,
                'username': user.username,
                'django_user_id': user.id
            })
        return JsonResponse({'success': False, 'message': '账号或密码错误'})
    return JsonResponse({'success': False, 'message': '无效请求'})
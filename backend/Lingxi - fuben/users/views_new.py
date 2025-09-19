from django.shortcuts import render

# Create your views here.
# users/views.py
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import UserProfile, EmailVerification
from .email_service import EmailService
import json
import uuid
import re
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def send_verification_code(request):
    """发送邮箱验证码"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        verification_type = data.get('type', 'register')  # register, password_reset, email_change
        
        if not email:
            return JsonResponse({'success': False, 'message': '邮箱地址不能为空'})
        
        # 验证邮箱格式
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({'success': False, 'message': '邮箱格式不正确'})
        
        # 检查验证类型
        if verification_type not in ['register', 'password_reset', 'email_change']:
            return JsonResponse({'success': False, 'message': '无效的验证类型'})
        
        # 注册验证：检查邮箱是否已被注册
        if verification_type == 'register':
            if User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': '该邮箱已被注册'})
        
        # 密码重置验证：检查邮箱是否已注册
        elif verification_type == 'password_reset':
            if not User.objects.filter(email=email).exists():
                return JsonResponse({'success': False, 'message': '该邮箱尚未注册'})
        
        # 发送验证码
        result = EmailService.send_verification_code(email, verification_type)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'message': '验证码发送成功，请查收邮件',
                'verification_id': result['verification_id']
            })
        else:
            return JsonResponse({'success': False, 'message': result['error']})
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '请求数据格式错误'})
    except Exception as e:
        logger.error(f"发送验证码错误: {str(e)}")
        return JsonResponse({'success': False, 'message': '发送验证码失败，请稍后重试'})

@csrf_exempt
def verify_email_code(request):
    """验证邮箱验证码"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        code = data.get('code', '').strip()
        verification_type = data.get('type', 'register')
        
        if not email or not code:
            return JsonResponse({'success': False, 'message': '邮箱和验证码不能为空'})
        
        # 验证码格式检查（6位数字）
        if not re.match(r'^\d{6}$', code):
            return JsonResponse({'success': False, 'message': '验证码格式不正确'})
        
        # 验证验证码
        result = EmailService.verify_code(email, code, verification_type)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'message': '验证成功',
                'verification_id': result['verification'].id
            })
        else:
            return JsonResponse({'success': False, 'message': result['error']})
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '请求数据格式错误'})
    except Exception as e:
        logger.error(f"验证邮箱验证码错误: {str(e)}")
        return JsonResponse({'success': False, 'message': '验证失败，请稍后重试'})

@csrf_exempt
def register(request):
    """用户注册（支持邮箱验证）"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        verification_code = data.get('verification_code', '').strip()
        nickname = data.get('nickname', '').strip() or username
        
        # 兼容旧版本（使用phoneNumber作为username）
        if not email and data.get('phoneNumber'):
            username = data.get('phoneNumber')
            email = None
        
        if not username or not password:
            return JsonResponse({'success': False, 'message': '用户名和密码不能为空'})
        
        # 如果提供了邮箱，需要验证邮箱验证码
        if email:
            if not verification_code:
                return JsonResponse({'success': False, 'message': '请输入邮箱验证码'})
            
            # 验证邮箱验证码
            verify_result = EmailService.verify_code(email, verification_code, 'register')
            if not verify_result['success']:
                return JsonResponse({'success': False, 'message': verify_result['error']})
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': '用户名已存在'})
        
        # 检查邮箱是否已被注册（如果提供了邮箱）
        if email and User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': '该邮箱已被注册'})
        
        # 创建用户
        user = User.objects.create_user(
            username=username, 
            password=password,
            email=email or ''
        )
        
        # 创建用户资料
        external_user_id = str(uuid.uuid4())
        profile = UserProfile.objects.create(
            user=user,
            nickname=nickname,
            external_user_id=external_user_id,
            email_verified=bool(email)  # 如果通过邮箱验证注册，标记为已验证
        )
        
        logger.info(f"用户注册成功: {username}, 邮箱: {email or '未提供'}")
        
        return JsonResponse({
            'success': True, 
            'message': '注册成功',
            'user_id': external_user_id,
            'username': username,
            'email_verified': profile.email_verified
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '请求数据格式错误'})
    except Exception as e:
        logger.error(f"用户注册错误: {str(e)}")
        return JsonResponse({'success': False, 'message': '注册失败，请稍后重试'})

@csrf_exempt
def login(request):
    """用户登录"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return JsonResponse({'success': False, 'message': '用户名和密码不能为空'})
        
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
                    external_user_id=external_user_id,
                    email_verified=bool(user.email)
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
            
            logger.info(f"用户登录成功: {username}")
            
            return JsonResponse({
                'success': True, 
                'menuList': menu_list, 
                'message': '登录成功',
                'user_id': profile.external_user_id,
                'username': user.username,
                'django_user_id': user.id,
                'email': user.email,
                'email_verified': profile.email_verified
            })
        else:
            return JsonResponse({'success': False, 'message': '账号或密码错误'})
            
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '请求数据格式错误'})
    except Exception as e:
        logger.error(f"用户登录错误: {str(e)}")
        return JsonResponse({'success': False, 'message': '登录失败，请稍后重试'})

@csrf_exempt
def reset_password(request):
    """重置密码"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': '只支持POST请求'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        verification_code = data.get('verification_code', '').strip()
        new_password = data.get('new_password', '').strip()
        
        if not email or not verification_code or not new_password:
            return JsonResponse({'success': False, 'message': '邮箱、验证码和新密码不能为空'})
        
        # 验证邮箱验证码
        verify_result = EmailService.verify_code(email, verification_code, 'password_reset')
        if not verify_result['success']:
            return JsonResponse({'success': False, 'message': verify_result['error']})
        
        # 查找用户
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': '用户不存在'})
        
        # 重置密码
        user.set_password(new_password)
        user.save()
        
        logger.info(f"密码重置成功: {email}")
        
        return JsonResponse({
            'success': True,
            'message': '密码重置成功，请使用新密码登录'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '请求数据格式错误'})
    except Exception as e:
        logger.error(f"密码重置错误: {str(e)}")
        return JsonResponse({'success': False, 'message': '密码重置失败，请稍后重试'})

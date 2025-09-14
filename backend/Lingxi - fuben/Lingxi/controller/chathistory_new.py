from django.shortcuts import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from lingxiapp.models import ChatSession, ChatMessage, UserPreference
from users.models import UserProfile
import json
import uuid
import requests
from datetime import datetime, timedelta
from django.utils import timezone

@csrf_exempt
def get_chat_history(request):
    """获取用户聊天历史记录"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    # 从请求头或session中获取用户标识
    user_id = request.GET.get('user_id')
    session_id = request.GET.get('session_id')
    
    if not user_id:
        # 如果没有用户ID，创建一个临时用户标识
        user_id = request.session.get('temp_user_id')
        if not user_id:
            user_id = str(uuid.uuid4())
            request.session['temp_user_id'] = user_id
    
    try:
        # 首先尝试通过external_user_id查找用户资料
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            # 如果不存在，创建新用户和资料
            # 使用完整的UUID作为用户名来避免冲突
            username = f'temp_user_{user_id}'
            user = User.objects.create(
                username=username,
                email=f'{user_id[:8]}@temp.local'
            )
            
            # 创建用户资料
            profile = UserProfile.objects.create(
                user=user,
                nickname='访客用户',
                external_user_id=user_id
            )
        
        # 获取活跃的聊天会话
        if session_id:
            try:
                chat_session = ChatSession.objects.get(session_id=session_id, user=user)
            except ChatSession.DoesNotExist:
                chat_session = ChatSession.objects.create(
                    user=user,
                    title=f'对话 {datetime.now().strftime("%m-%d %H:%M")}'
                )
        else:
            # 获取最近的活跃会话或创建新会话
            chat_session = ChatSession.objects.filter(user=user, is_active=True).first()
            if not chat_session:
                chat_session = ChatSession.objects.create(
                    user=user,
                    title=f'对话 {datetime.now().strftime("%m-%d %H:%M")}'
                )
        
        # 获取最近20条消息
        messages = ChatMessage.objects.filter(
            session=chat_session
        ).order_by('-timestamp')[:20]
        
        # 转换为前端格式
        message_list = []
        for msg in reversed(messages):  # 反转以获得正确的时间顺序
            message_list.append({
                'id': str(msg.message_id),
                'text': msg.content,
                'isUser': msg.message_type == 'user',
                'timestamp': msg.timestamp.isoformat(),
                'emotion': msg.emotion
            })
        
        return JsonResponse({
            'success': True,
            'messages': message_list,
            'session_id': str(chat_session.session_id),
            'user_id': str(profile.external_user_id)
        })
        
    except Exception as e:
        print(f"获取聊天历史错误: {e}")
        return JsonResponse({'error': '获取聊天历史失败'}, status=500)

@csrf_exempt
def save_chat_message(request):
    """保存聊天消息"""
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        params = json.loads(request.body)
        user_id = params.get('user_id')
        session_id = params.get('session_id')
        message_type = params.get('message_type', 'user')
        content = params.get('content', '')
        emotion = params.get('emotion')
        
        if not user_id or not session_id or not content:
            return JsonResponse({'error': '缺少必要参数'}, status=400)
        
        # 获取用户和会话
        profile = UserProfile.objects.get(external_user_id=user_id)
        user = profile.user
        chat_session = ChatSession.objects.get(session_id=session_id, user=user)
        
        # 创建消息记录
        message = ChatMessage.objects.create(
            session=chat_session,
            user=user,
            message_type=message_type,
            content=content,
            emotion=emotion
        )
        
        # 更新会话的最后更新时间
        chat_session.updated_at = timezone.now()
        chat_session.save()
        
        return JsonResponse({
            'success': True,
            'message_id': str(message.message_id),
            'timestamp': message.timestamp.isoformat()
        })
        
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': '用户不存在'}, status=404)
    except ChatSession.DoesNotExist:
        return JsonResponse({'error': '会话不存在'}, status=404)
    except Exception as e:
        print(f"保存消息错误: {e}")
        return JsonResponse({'error': '保存消息失败'}, status=500)

@csrf_exempt
def enhanced_chat(request):
    """增强的聊天API，支持消息历史记录"""
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        params = json.loads(request.body)
        user_message = params.get('prompt', '')
        system_prompt = params.get('system', '')
        user_id = params.get('user_id')
        session_id = params.get('session_id')
        
        # 获取或创建用户
        if not user_id:
            user_id = request.session.get('temp_user_id')
            if not user_id:
                user_id = str(uuid.uuid4())
                request.session['temp_user_id'] = user_id
        
        # 首先尝试通过external_user_id查找用户资料
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            # 如果不存在，创建新用户和资料
            # 使用完整的UUID作为用户名来避免冲突
            username = f'temp_user_{user_id}'
            user = User.objects.create(
                username=username,
                email=f'{user_id[:8]}@temp.local'
            )
            
            # 创建用户资料
            profile = UserProfile.objects.create(
                user=user,
                nickname='访客用户',
                external_user_id=user_id
            )
        
        # 获取或创建会话
        if session_id:
            try:
                chat_session = ChatSession.objects.get(session_id=session_id, user=user)
            except ChatSession.DoesNotExist:
                chat_session = ChatSession.objects.create(
                    user=user,
                    title=f'对话 {datetime.now().strftime("%m-%d %H:%M")}'
                )
        else:
            chat_session = ChatSession.objects.filter(user=user, is_active=True).first()
            if not chat_session:
                chat_session = ChatSession.objects.create(
                    user=user,
                    title=f'对话 {datetime.now().strftime("%m-%d %H:%M")}'
                )
        
        # 保存用户消息
        user_msg = ChatMessage.objects.create(
            session=chat_session,
            user=user,
            message_type='user',
            content=user_message
        )
        
        # 构建历史对话上下文
        recent_messages = ChatMessage.objects.filter(
            session=chat_session
        ).order_by('-timestamp')[:10]  # 获取最近10条消息作为上下文
        
        history = []
        for msg in reversed(recent_messages[:-1]):  # 排除刚刚保存的用户消息
            if msg.message_type == 'user':
                history.append({"role": "user", "content": msg.content})
            elif msg.message_type == 'ai':
                history.append({"role": "assistant", "content": msg.content})
        
        # 调用AI模型
        headers = {'Content-Type': 'application/json'}
        data = {
            "text": user_message,
            "system": system_prompt,
            "history": history
        }
        
        print(f"发送到AI模型的数据: {data}")
        
        res = requests.post(
            url='http://localhost:25674/chat/',
            headers=headers,
            data=json.dumps(data),
            timeout=30
        )
        
        ai_response = res.json()
        ai_content = ai_response.get('result', '抱歉，我暂时无法回复。')
        
        # 保存AI回复
        ai_msg = ChatMessage.objects.create(
            session=chat_session,
            user=user,
            message_type='ai',
            content=ai_content
        )
        
        # 更新会话
        chat_session.updated_at = timezone.now()
        chat_session.save()
        
        # 返回完整响应
        return JsonResponse({
            'result': ai_content,
            'session_id': str(chat_session.session_id),
            'user_id': str(profile.external_user_id),
            'message_id': str(ai_msg.message_id),
            'timestamp': ai_msg.timestamp.isoformat()
        })
        
    except Exception as e:
        print(f"聊天API错误: {e}")
        return JsonResponse({
            'error': '聊天服务暂时不可用',
            'result': '抱歉，我现在无法正常回复。请稍后再试。'
        }, status=500)

@csrf_exempt
def get_user_sessions(request):
    """获取用户的所有会话列表"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({'error': '缺少用户ID'}, status=400)
    
    try:
        profile = UserProfile.objects.get(external_user_id=user_id)
        user = profile.user
        sessions = ChatSession.objects.filter(user=user).order_by('-updated_at')[:10]
        
        session_list = []
        for session in sessions:
            last_message = ChatMessage.objects.filter(session=session).order_by('-timestamp').first()
            session_list.append({
                'session_id': str(session.session_id),
                'title': session.title,
                'created_at': session.created_at.isoformat(),
                'updated_at': session.updated_at.isoformat(),
                'message_count': ChatMessage.objects.filter(session=session).count(),
                'last_message': last_message.content[:50] + '...' if last_message else '暂无消息',
                'is_active': session.is_active
            })
        
        return JsonResponse({
            'success': True,
            'sessions': session_list
        })
        
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': '用户不存在'}, status=404)
    except Exception as e:
        print(f"获取会话列表错误: {e}")
        return JsonResponse({'error': '获取会话列表失败'}, status=500)

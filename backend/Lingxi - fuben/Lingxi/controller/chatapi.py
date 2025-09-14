from ..system.tools import jsonutil
from django.shortcuts import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse
from django.contrib.auth.models import User
from lingxiapp.models import ChatSession, ChatMessage
from users.models import UserProfile
import uuid
from datetime import datetime
from django.utils import timezone

@csrf_exempt
def getchat(request):
    print("开始获取对话")                                #在终端中输出开始对话，表示函数开始运行
    headers = {'Content-Type': 'application/json'}    #http请求头部
    params = json.loads(request.body)                 #读取request请求中的数据包
    print(params)                                     #在终端中输出请求，表示数据接受正常
    history = []
    data = {                                          #创建向服务器发送的数据包，包含三个变量"text"、"system"和"history"
        "text": params['prompt'],
        "system": params['system'],
        "history": history
    }
    print(data)                                       #在终端中打印数据包，表示程序正常运行
    res = requests.post(                              #向服务器发送请求，并将返回的数据存储在"res"变量中
                 url='http://localhost:25674/chat/',
                 headers=headers,
                 data=json.dumps(data))
    print("完成生成")                                   #在终端中输出完成生成，表示模型成功生成回复并发送成功，程序运行正常
    d = res.json()                                    #将返回文件打包为 json
    return JsonResponse(d)                            #返回请求

@csrf_exempt
def enhanced_chat(request):
    """增强的聊天API，支持消息历史记录"""
    print("开始增强对话")
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        params = json.loads(request.body)
        user_message = params.get('prompt', '')
        system_prompt = params.get('system', '')
        user_id = params.get('user_id')
        session_id = params.get('session_id')
        
        print(f"接收到参数: user_id={user_id}, session_id={session_id}")
          # 获取或创建用户
        if not user_id:
            user_id = str(uuid.uuid4())
        
        # 确保user_id是有效的UUID格式
        try:
            uuid.UUID(user_id)  # 验证UUID格式
        except ValueError:
            # 如果不是有效UUID，生成一个新的
            user_id = str(uuid.uuid4())
        
        user, created = User.objects.get_or_create(
            username=f'user_{user_id[:8]}',  # 使用UUID前8位作为用户名
            defaults={
                'email': f'{user_id[:8]}@temp.local'
            }
        )
        
        # 创建或获取用户资料
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'nickname': '访客用户',
                'external_user_id': user_id
            }
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
        
        # 构建历史对话上下文（最近5条）
        recent_messages = ChatMessage.objects.filter(
            session=chat_session
        ).order_by('-timestamp')[:6]  # 多获取一条用于排除当前消息
        
        history = []
        for msg in reversed(recent_messages[1:]):  # 排除刚刚保存的用户消息
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
        
        print(f"发送到AI模型: {data}")
        
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
        
        print("完成增强对话生成")
        
        # 返回完整响应
        return JsonResponse({
            'result': ai_content,
            'session_id': str(chat_session.session_id),
            'user_id': str(profile.external_user_id),
            'message_id': str(ai_msg.message_id),
            'timestamp': ai_msg.timestamp.isoformat()
        })
        
    except Exception as e:
        print(f"增强聊天API错误: {e}")
        return JsonResponse({
            'error': '聊天服务暂时不可用',
            'result': '抱歉，我现在无法正常回复。请稍后再试。'
        }, status=500)

@csrf_exempt
def get_chat_history(request):
    """获取用户聊天历史记录"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    user_id = request.GET.get('user_id')
    session_id = request.GET.get('session_id')
    
    try:
        if not user_id:
            return JsonResponse({
                'success': True,
                'messages': [],
                'session_id': '',
                'user_id': ''
            })
        
        # 验证UUID格式
        try:
            uuid.UUID(user_id)
        except ValueError:
            return JsonResponse({
                'success': True,
                'messages': [],
                'session_id': '',
                'user_id': user_id
            })
        
        # 获取用户
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({
                'success': True,
                'messages': [],
                'session_id': '',
                'user_id': user_id
            })
        
        # 获取会话
        if session_id:
            try:
                chat_session = ChatSession.objects.get(session_id=session_id, user=user)
            except ChatSession.DoesNotExist:
                return JsonResponse({
                    'success': True,
                    'messages': [],
                    'session_id': '',
                    'user_id': user_id
                })
        else:
            chat_session = ChatSession.objects.filter(user=user, is_active=True).first()
            if not chat_session:
                return JsonResponse({
                    'success': True,
                    'messages': [],
                    'session_id': '',
                    'user_id': user_id
                })
        
        # 获取最近20条消息
        messages = ChatMessage.objects.filter(
            session=chat_session
        ).order_by('-timestamp')[:20]
        
        # 转换为前端格式
        message_list = []
        for msg in reversed(messages):
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
            'user_id': user_id
        })
        
    except Exception as e:
        print(f"获取聊天历史错误: {e}")
        return JsonResponse({'error': '获取聊天历史失败'}, status=500)

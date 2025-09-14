#!/usr/bin/env python
import os
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from lingxiapp.models import ChatSession, ChatMessage

print("=== 用户隔离功能测试 ===")

def test_user_login(username, password):
    """测试用户登录并返回user_id"""
    print(f"\n--- 测试用户登录: {username} ---")
    
    try:
        response = requests.post('http://127.0.0.1:8000/appp/login/', 
                               json={'username': username, 'password': password},
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ 登录成功: {data.get('message')}")
                print(f"   用户ID: {data.get('user_id')}")
                print(f"   Django用户ID: {data.get('django_user_id')}")
                return data.get('user_id'), data.get('django_user_id')
            else:
                print(f"❌ 登录失败: {data.get('message')}")
                return None, None
        else:
            print(f"❌ 登录请求失败: HTTP {response.status_code}")
            return None, None
    except Exception as e:
        print(f"❌ 登录异常: {e}")
        return None, None

def test_chat_message(user_id, message):
    """测试发送聊天消息"""
    print(f"\n--- 测试发送消息: {message[:20]}... ---")
      try:
        response = requests.post('http://127.0.0.1:8000/enhanced-chat/', 
                               json={
                                   'prompt': message,
                                   'system': '你是一个友好的助手',
                                   'user_id': str(user_id)  # 确保转换为字符串
                               },
                               headers={'Content-Type': 'application/json'})
        
        print(f"HTTP状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('result'):
                print(f"✅ 消息发送成功")
                print(f"   会话ID: {data.get('session_id')}")
                print(f"   消息ID: {data.get('message_id')}")
                print(f"   AI回复: {data.get('result')[:50]}...")
                return data.get('session_id')
            else:
                print(f"❌ 消息处理失败: {data}")
                return None
        else:
            print(f"❌ 消息发送失败: HTTP {response.status_code}")
            print(f"   响应内容: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 消息发送异常: {e}")
        return None

def test_chat_history(user_id, session_id=None):
    """测试获取聊天历史"""
    print(f"\n--- 测试获取聊天历史 ---")
    
    try:
        params = {'user_id': user_id}
        if session_id:
            params['session_id'] = session_id
            
        response = requests.get('http://127.0.0.1:8000/chat-history/', 
                               params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                messages = data.get('messages', [])
                print(f"✅ 获取历史成功，找到 {len(messages)} 条消息")
                for i, msg in enumerate(messages[-3:]):  # 只显示最后3条
                    print(f"   消息{i+1}: {'用户' if msg['isUser'] else 'AI'} - {msg['text'][:30]}...")
                return True
            else:
                print(f"❌ 获取历史失败: {data}")
                return False
        else:
            print(f"❌ 获取历史失败: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 获取历史异常: {e}")
        return False

def check_database_isolation():
    """检查数据库中的用户隔离情况"""
    print(f"\n--- 检查数据库隔离情况 ---")
    
    users = User.objects.all()
    print(f"总用户数: {users.count()}")
    
    for user in users:
        try:
            profile = UserProfile.objects.get(user=user)
            sessions = ChatSession.objects.filter(user=user).count()
            messages = ChatMessage.objects.filter(user=user).count()
            print(f"  用户{user.id}({user.username}): 外部ID={str(profile.external_user_id)[:8]}..., 会话={sessions}, 消息={messages}")
        except UserProfile.DoesNotExist:
            print(f"  用户{user.id}({user.username}): ❌ 缺少UserProfile")

# 开始测试
print("开始用户隔离功能完整测试...")

# 1. 检查初始数据库状态
check_database_isolation()

# 2. 测试用户14（zhnagtao）登录
user_id_14, django_id_14 = test_user_login('zhnagtao', 'password_if_set')

# 3. 测试用户15（li）登录  
user_id_15, django_id_15 = test_user_login('li', 'password_if_set')

# 4. 如果登录失败，使用已知的external_user_id进行测试
if not user_id_14:
    try:
        profile_14 = UserProfile.objects.get(user__id=14)
        user_id_14 = profile_14.external_user_id
        print(f"使用数据库中的用户14 external_user_id: {user_id_14}")
    except:
        print("无法获取用户14的external_user_id")

if not user_id_15:
    try:
        profile_15 = UserProfile.objects.get(user__id=15)
        user_id_15 = profile_15.external_user_id
        print(f"使用数据库中的用户15 external_user_id: {user_id_15}")
    except:
        print("无法获取用户15的external_user_id")

# 5. 测试用户14发送消息
if user_id_14:
    session_id_14 = test_chat_message(user_id_14, "你好，我是用户14，这是我的第一条消息")
    
# 6. 测试用户15发送消息
if user_id_15:
    session_id_15 = test_chat_message(user_id_15, "你好，我是用户15，这是我的测试消息")

# 7. 测试获取各自的聊天历史
if user_id_14:
    test_chat_history(user_id_14)
    
if user_id_15:
    test_chat_history(user_id_15)

# 8. 再次检查数据库状态
print(f"\n=== 测试后数据库状态 ===")
check_database_isolation()

print(f"\n=== 测试完成 ===")
print("如果看到不同用户的消息数量分别增加，说明用户隔离功能正常工作！")

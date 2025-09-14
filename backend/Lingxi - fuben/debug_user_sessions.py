#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from lingxiapp.models import ChatSession, ChatMessage
from datetime import datetime

print("=== 用户14和15的详细会话调试 ===")

# 检查用户14
print("\n=== 用户14 (zhnagtao) 详细信息 ===")
try:
    user_14 = User.objects.get(id=14)
    profile_14 = UserProfile.objects.get(user=user_14)
    print(f"用户14: {user_14.username}, 外部ID: {profile_14.external_user_id}")
    
    sessions_14 = ChatSession.objects.filter(user=user_14).order_by('-updated_at')
    print(f"用户14的会话数: {sessions_14.count()}")
    
    for session in sessions_14:
        print(f"  会话ID: {session.session_id}")
        print(f"  标题: {session.title}")
        print(f"  创建时间: {session.created_at}")
        print(f"  更新时间: {session.updated_at}")
        print(f"  是否活跃: {session.is_active}")
        
        messages_14 = ChatMessage.objects.filter(session=session).order_by('timestamp')
        print(f"  该会话中的消息数: {messages_14.count()}")
        
        for msg in messages_14:
            print(f"    [{msg.timestamp.strftime('%H:%M:%S')}] {msg.message_type}: {msg.content[:50]}...")
        print()
        
except Exception as e:
    print(f"用户14检查失败: {e}")

# 检查用户15
print("\n=== 用户15 (li) 详细信息 ===")
try:
    user_15 = User.objects.get(id=15)
    profile_15 = UserProfile.objects.get(user=user_15)
    print(f"用户15: {user_15.username}, 外部ID: {profile_15.external_user_id}")
    
    sessions_15 = ChatSession.objects.filter(user=user_15).order_by('-updated_at')
    print(f"用户15的会话数: {sessions_15.count()}")
    
    for session in sessions_15:
        print(f"  会话ID: {session.session_id}")
        print(f"  标题: {session.title}")
        print(f"  创建时间: {session.created_at}")
        print(f"  更新时间: {session.updated_at}")
        print(f"  是否活跃: {session.is_active}")
        
        messages_15 = ChatMessage.objects.filter(session=session).order_by('timestamp')
        print(f"  该会话中的消息数: {messages_15.count()}")
        
        for msg in messages_15:
            print(f"    [{msg.timestamp.strftime('%H:%M:%S')}] {msg.message_type}: {msg.content[:50]}...")
        print()
        
except Exception as e:
    print(f"用户15检查失败: {e}")

# 检查最近的消息时间戳
print("\n=== 最近消息时间分析 ===")
recent_messages = ChatMessage.objects.all().order_by('-timestamp')[:10]
for msg in recent_messages:
    user_name = msg.user.username
    print(f"[{msg.timestamp.strftime('%m-%d %H:%M:%S')}] 用户{msg.user.id}({user_name}): {msg.message_type} - {msg.content[:30]}...")

print("\n=== 调试完成 ===")

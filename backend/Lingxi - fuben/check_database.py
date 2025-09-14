#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from lingxiapp.models import ChatSession, ChatMessage

print("=== 数据库状态检查 ===")

# 检查用户表
users = User.objects.all()
print(f"\n用户表 (User) - 总数: {users.count()}")
for user in users:
    print(f"  用户ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}")

# 检查用户资料表
profiles = UserProfile.objects.all()
print(f"\n用户资料表 (UserProfile) - 总数: {profiles.count()}")
for profile in profiles:
    print(f"  资料ID: {profile.id}, 用户ID: {profile.user.id}, 外部ID: {profile.external_user_id}, 昵称: {profile.nickname}")

# 检查聊天会话表
sessions = ChatSession.objects.all()
print(f"\n聊天会话表 (ChatSession) - 总数: {sessions.count()}")
for session in sessions:
    print(f"  会话ID: {session.session_id}, 用户ID: {session.user.id}, 标题: {session.title}")

# 检查聊天消息表
messages = ChatMessage.objects.all()
print(f"\n聊天消息表 (ChatMessage) - 总数: {messages.count()}")
for message in messages[:10]:  # 只显示前10条
    print(f"  消息ID: {message.message_id}, 用户ID: {message.user.id}, 类型: {message.message_type}, 内容: {message.content[:30]}...")

if messages.count() > 10:
    print(f"  ... 还有 {messages.count() - 10} 条消息")

# 检查用户16的数据
print(f"\n=== 用户ID 16 的详细信息 ===")
try:
    user_16 = User.objects.get(id=16)
    print(f"用户16: {user_16.username}, 邮箱: {user_16.email}")
    
    try:
        profile_16 = UserProfile.objects.get(user=user_16)
        print(f"用户16的资料: external_user_id={profile_16.external_user_id}, 昵称={profile_16.nickname}")
    except UserProfile.DoesNotExist:
        print("用户16没有对应的UserProfile!")
    
    sessions_16 = ChatSession.objects.filter(user=user_16)
    print(f"用户16的会话数: {sessions_16.count()}")
    
    messages_16 = ChatMessage.objects.filter(user=user_16)
    print(f"用户16的消息数: {messages_16.count()}")
    
except User.DoesNotExist:
    print("用户ID 16 不存在!")

# 检查用户12的数据
print(f"\n=== 用户ID 12 的详细信息 ===")
try:
    user_12 = User.objects.get(id=12)
    print(f"用户12: {user_12.username}, 邮箱: {user_12.email}")
    
    try:
        profile_12 = UserProfile.objects.get(user=user_12)
        print(f"用户12的资料: external_user_id={profile_12.external_user_id}, 昵称={profile_12.nickname}")
    except UserProfile.DoesNotExist:
        print("用户12没有对应的UserProfile!")
    
    sessions_12 = ChatSession.objects.filter(user=user_12)
    print(f"用户12的会话数: {sessions_12.count()}")
    
    messages_12 = ChatMessage.objects.filter(user=user_12)
    print(f"用户12的消息数: {messages_12.count()}")
    
except User.DoesNotExist:
    print("用户ID 12 不存在!")

print("\n=== 检查完成 ===")

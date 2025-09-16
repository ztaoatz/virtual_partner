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

print("=== 详细检查聊天消息时间戳 ===")

# 获取所有消息并显示时间戳
messages = ChatMessage.objects.all().order_by('-timestamp')
print(f"总消息数: {messages.count()}")

print("\n前10条消息的详细信息:")
for msg in messages[:10]:
    user_id = msg.user.id
    msg_date = msg.timestamp.date()
    msg_time = msg.timestamp.time()
    print(f"用户ID: {user_id}, 日期: {msg_date}, 时间: {msg_time}, 类型: {msg.message_type}, 内容: {msg.content[:30]}...")

# 按用户和日期统计
print("\n=== 按用户和日期统计 ===")
for user_id in [12, 14, 15, 16]:
    try:
        user = User.objects.get(id=user_id)
        user_messages = ChatMessage.objects.filter(user=user)
        
        if user_messages.exists():
            print(f"\n用户 {user.username} (ID: {user_id}):")
            # 按日期分组
            dates = {}
            for msg in user_messages:
                date_str = msg.timestamp.date().strftime('%Y-%m-%d')
                if date_str not in dates:
                    dates[date_str] = 0
                dates[date_str] += 1
            
            for date, count in sorted(dates.items()):
                print(f"  {date}: {count} 条消息")
                
                # 获取该用户对应的external_user_id
                try:
                    profile = UserProfile.objects.get(user=user)
                    external_id = profile.external_user_id
                    
                    # 测试该日期是否有足够的消息生成日记
                    if count >= 2:
                        print(f"    -> 可以生成日记 (external_id: {external_id})")
                    else:
                        print(f"    -> 消息太少，无法生成日记")
                except UserProfile.DoesNotExist:
                    print(f"    -> 没有对应的UserProfile")
        else:
            print(f"\n用户 {user.username} (ID: {user_id}): 没有消息")
    except User.DoesNotExist:
        print(f"用户ID {user_id} 不存在")

print("\n=== 检查完成 ===")

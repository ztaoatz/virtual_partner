#!/usr/bin/env python
import os
import django
import requests
import json

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from users.models import UserProfile

print("=== 测试聊天历史加载API ===")

# 获取用户14和15的external_user_id
try:
    profile_14 = UserProfile.objects.get(user_id=14)
    profile_15 = UserProfile.objects.get(user_id=15)
    
    user_14_external_id = profile_14.external_user_id
    user_15_external_id = profile_15.external_user_id
    
    print(f"用户14的external_user_id: {user_14_external_id}")
    print(f"用户15的external_user_id: {user_15_external_id}")
    
    # 测试用户14的聊天历史加载
    print("\n=== 测试用户14聊天历史加载 ===")
    response_14 = requests.get('http://127.0.0.1:8000/chat-history/', params={
        'user_id': user_14_external_id
    })
    
    if response_14.status_code == 200:
        data_14 = response_14.json()
        print(f"用户14请求成功: {data_14.get('success')}")
        print(f"返回的user_id: {data_14.get('user_id')}")
        print(f"返回的session_id: {data_14.get('session_id')}")
        print(f"消息数量: {len(data_14.get('messages', []))}")
        
        if data_14.get('messages'):
            print("消息内容:")
            for msg in data_14['messages']:
                print(f"  [{msg['timestamp'][:19]}] {'用户' if msg['isUser'] else 'AI'}: {msg['text'][:50]}...")
    else:
        print(f"用户14请求失败: {response_14.status_code} - {response_14.text}")
    
    # 测试用户15的聊天历史加载
    print("\n=== 测试用户15聊天历史加载 ===")
    response_15 = requests.get('http://127.0.0.1:8000/chat-history/', params={
        'user_id': user_15_external_id
    })
    
    if response_15.status_code == 200:
        data_15 = response_15.json()
        print(f"用户15请求成功: {data_15.get('success')}")
        print(f"返回的user_id: {data_15.get('user_id')}")
        print(f"返回的session_id: {data_15.get('session_id')}")
        print(f"消息数量: {len(data_15.get('messages', []))}")
        
        if data_15.get('messages'):
            print("消息内容:")
            for msg in data_15['messages']:
                print(f"  [{msg['timestamp'][:19]}] {'用户' if msg['isUser'] else 'AI'}: {msg['text'][:50]}...")
    else:
        print(f"用户15请求失败: {response_15.status_code} - {response_15.text}")
    
    # 测试不存在的用户
    print("\n=== 测试不存在的用户 ===")
    fake_user_id = "00000000-0000-0000-0000-000000000000"
    response_fake = requests.get('http://127.0.0.1:8000/chat-history/', params={
        'user_id': fake_user_id
    })
    
    if response_fake.status_code == 200:
        data_fake = response_fake.json()
        print(f"虚假用户请求成功: {data_fake.get('success')}")
        print(f"返回的user_id: {data_fake.get('user_id')}")
        print(f"消息数量: {len(data_fake.get('messages', []))}")
    else:
        print(f"虚假用户请求失败: {response_fake.status_code}")
        
except Exception as e:
    print(f"测试失败: {e}")

print("\n=== 测试完成 ===")

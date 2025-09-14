#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试聊天历史加载功能
验证用户登录后能否正确加载其历史聊天记录
"""

import os
import sys
import django
import requests
import json

# 设置Django环境
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from lingxiapp.models import ChatSession, ChatMessage

def test_chat_history_loading():
    """测试聊天历史加载功能"""
    print("=== 测试聊天历史加载功能 ===")
    
    # 获取现有用户数据
    users_with_messages = []
    for profile in UserProfile.objects.all():
        user = profile.user
        message_count = ChatMessage.objects.filter(user=user).count()
        if message_count > 0:
            users_with_messages.append({
                'user_id': user.id,
                'external_user_id': profile.external_user_id,
                'username': user.username,
                'nickname': profile.nickname,
                'message_count': message_count
            })
    
    print(f"找到 {len(users_with_messages)} 个有聊天记录的用户:")
    for user_info in users_with_messages:
        print(f"  - 用户ID: {user_info['user_id']}, 外部ID: {user_info['external_user_id']}")
        print(f"    用户名: {user_info['username']}, 昵称: {user_info['nickname']}")
        print(f"    消息数量: {user_info['message_count']}")
        print()
    
    # 测试每个用户的聊天历史加载
    for user_info in users_with_messages:
        print(f"=== 测试用户 {user_info['username']} 的聊天历史加载 ===")
        
        # 测试不带session_id的请求（模拟用户登录后首次访问）
        test_url = "http://127.0.0.1:8000/chat-history/"
        params = {
            'user_id': user_info['external_user_id']
        }
        
        try:
            response = requests.get(test_url, params=params)
            print(f"请求URL: {test_url}")
            print(f"请求参数: {params}")
            print(f"响应状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"响应数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
                
                if data.get('success'):
                    messages = data.get('messages', [])
                    print(f"✅ 成功加载 {len(messages)} 条历史消息")
                    
                    if messages:
                        print("最近的几条消息:")
                        for i, msg in enumerate(messages[-3:], 1):  # 显示最后3条消息
                            msg_type = "用户" if msg['isUser'] else "AI"
                            print(f"  {i}. [{msg_type}] {msg['text'][:50]}...")
                    
                    # 验证返回的user_id和session_id
                    returned_user_id = data.get('user_id')
                    returned_session_id = data.get('session_id')
                    print(f"返回的用户ID: {returned_user_id}")
                    print(f"返回的会话ID: {returned_session_id}")
                else:
                    print(f"❌ 请求失败: {data}")
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应内容: {response.text}")
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
        
        print("-" * 60)
    
    # 测试新用户（无历史记录）
    print("=== 测试新用户（无历史记录）===")
    new_user_id = "test-new-user-12345-67890"
    params = {'user_id': new_user_id}
    
    try:
        response = requests.get(test_url, params=params)
        print(f"新用户请求参数: {params}")
        print(f"响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"新用户响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get('success'):
                messages = data.get('messages', [])
                print(f"新用户消息数量: {len(messages)} (应该为0)")
                
                if len(messages) == 0:
                    print("✅ 新用户正确返回空消息列表")
                else:
                    print("❌ 新用户不应该有历史消息")
            
    except Exception as e:
        print(f"❌ 新用户测试异常: {e}")

if __name__ == '__main__':
    test_chat_history_loading()

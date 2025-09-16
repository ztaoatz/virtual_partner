#!/usr/bin/env python
import os
import django
import requests
import json
from datetime import datetime

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
from lingxiapp.models import ChatSession, ChatMessage

print("=== 测试情绪日记生成功能 ===")

# 测试用户
test_users = [
    {
        'id': 14,
        'external_id': '26368a8b-03cd-4f64-b73e-c37dcb0d5f0e',
        'username': 'zhnagtao'
    },
    {
        'id': 15,
        'external_id': '44852831-3cad-4ed6-9857-8e796c5c334c',
        'username': 'li'
    }
]

for test_user in test_users:
    print(f"\n--- 测试用户 {test_user['username']} (ID: {test_user['id']}) ---")    # 获取用户的聊天记录
    target_date = '2025-09-14'  # 测试2025年9月14日的数据
    messages = ChatMessage.objects.filter(
        user_id=test_user['id'],
        timestamp__date=target_date
    )
    
    print(f"今日消息数: {messages.count()}")
    
    if messages.count() > 0:
        print("消息内容:")
        for msg in messages[:5]:  # 显示前5条
            print(f"  - {msg.message_type}: {msg.content[:50]}...")
        
        # 测试生成情绪日记
        try:
            print("\n测试生成情绪日记...")
            response = requests.post(
                'http://127.0.0.1:8000/generate-diary/',                json={
                    'user_id': test_user['external_id'],
                    'date': target_date,
                    'force_regenerate': True
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    diary = result['diary']
                    print(f"✅ 日记生成成功!")
                    print(f"   内容长度: {len(diary['content'])} 字符")
                    print(f"   主要情绪: {diary['emotions']}")
                    print(f"   主要话题: {diary['main_topic']}")
                    print(f"   消息数量: {diary['message_count']}")
                    print(f"   日记内容预览: {diary['content'][:100]}...")
                else:
                    print(f"❌ 日记生成失败: {result.get('error')}")
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"   错误: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ 请求异常: {e}")
    else:
        print("今日没有聊天记录，跳过测试")

print("\n=== 测试Ollama代理健康检查 ===")
try:
    health_response = requests.get('http://localhost:25674/health', timeout=5)
    if health_response.status_code == 200:
        health_data = health_response.json()
        print(f"✅ Ollama代理服务正常")
        print(f"   状态: {health_data.get('status')}")
        print(f"   Ollama连接: {health_data.get('ollama')}")
    else:
        print(f"❌ Ollama代理健康检查失败: {health_response.status_code}")
except Exception as e:
    print(f"❌ Ollama代理服务连接失败: {e}")

print("\n=== 测试完成 ===")

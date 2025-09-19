#!/usr/bin/env python
import os
import django
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

import requests
import json
from datetime import datetime
from django.utils import timezone

def test_timezone_in_api():
    """测试API中的时区处理"""
    print("=== 测试时区修复后的API行为 ===")
    
    # 测试用户ID (li用户)
    user_id = "44852831-3cad-4ed6-9857-8e796c5c334c"
    
    print(f"当前本地时间: {datetime.now()}")
    print(f"当前Django时间: {timezone.now()}")
    print(f"当前Django本地时间: {timezone.localtime(timezone.now())}")
    
    # 1. 测试获取聊天历史
    print(f"\n1. 测试获取聊天历史...")
    try:
        response = requests.get('http://127.0.0.1:8000/chat-history/', {
            'user_id': user_id
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ 成功获取历史记录")
            print(f"   消息数量: {len(data.get('messages', []))}")
            
            # 检查最新消息的时间戳
            messages = data.get('messages', [])
            if messages:
                latest_msg = messages[-1]
                print(f"   最新消息时间: {latest_msg.get('timestamp')}")
                print(f"   最新消息内容: {latest_msg.get('text', '')[:50]}...")
        else:
            print(f"   ❌ 请求失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 请求异常: {e}")
      # 2. 测试发送消息 (检查新消息的时间戳)
    print(f"\n2. 测试发送消息...")
    try:
        test_message = f"时区测试消息 - {datetime.now().strftime('%H:%M:%S')}"
        response = requests.post('http://127.0.0.1:8000/chat/', 
            json={
                'prompt': test_message,
                'system': '你是一个友善的AI助手',
                'user_id': user_id,
                'session_id': None
            }, 
            headers={'Content-Type': 'application/json'},
            timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ 消息发送成功")
            print(f"   用户消息时间: {data.get('user_message', {}).get('timestamp')}")
            print(f"   AI回复时间: {data.get('ai_response', {}).get('timestamp')}")
        else:
            print(f"   ❌ 发送失败: {response.status_code}")
            print(f"   错误信息: {response.text}")
    except Exception as e:
        print(f"   ❌ 发送异常: {e}")
    
    # 3. 测试获取日记 (检查日记时间显示)
    print(f"\n3. 测试获取今日日记...")
    try:
        today = datetime.now().strftime('%Y-%m-%d')
        response = requests.get('http://127.0.0.1:8000/get-diary/', {
            'user_id': user_id,
            'date': today
        }, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                diary = data.get('diary', {})
                print(f"   ✓ 找到今日日记")
                print(f"   日记日期: {diary.get('date')}")
                print(f"   消息数量: {diary.get('message_count')}")
            else:
                print(f"   ℹ️  今日暂无日记")
        else:
            print(f"   ❌ 获取失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 获取异常: {e}")

if __name__ == '__main__':
    test_timezone_in_api()

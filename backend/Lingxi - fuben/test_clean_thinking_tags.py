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

print("=== 测试情绪日记思考标签清理功能 ===")

# 测试用户
test_user = {
    'external_id': '26368a8b-03cd-4f64-b73e-c37dcb0d5f0e',  # 用户14
    'username': 'zhnagtao'
}

# 使用2025-09-15的数据（这个日期有最新的消息）
target_date = '2025-09-15'

print(f"测试用户: {test_user['username']}")
print(f"目标日期: {target_date}")

try:
    print("\n正在生成情绪日记...")
    response = requests.post(
        'http://127.0.0.1:8000/generate-diary/',
        json={
            'user_id': test_user['external_id'],
            'date': target_date,
            'force_regenerate': True  # 强制重新生成以测试新的清理功能
        },
        timeout=120
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
            
            # 检查是否还有思考标签
            content = diary['content']
            if '<think>' in content or '</think>' in content:
                print("❌ 警告: 日记内容中仍然包含思考标签!")
                print("包含思考标签的部分:")
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '<think>' in line or '</think>' in line:
                        print(f"   第{i+1}行: {line}")
            else:
                print("✅ 思考标签已成功清理!")
            
            print(f"\n日记完整内容:")
            print("=" * 50)
            print(content)
            print("=" * 50)
        else:
            print(f"❌ 日记生成失败: {result.get('error')}")
    else:
        print(f"❌ API调用失败: {response.status_code}")
        print(f"   错误: {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"❌ 请求异常: {e}")

print("\n=== 测试完成 ===")

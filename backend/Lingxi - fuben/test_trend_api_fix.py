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
from users.models import UserProfile

def test_trend_api_fix():
    """测试趋势图API修复效果"""
    print("=== 测试趋势图API修复效果 ===")
    
    base_url = "http://127.0.0.1:8000/emotion-trend/"
    
    # 1. 测试不存在的用户ID
    print("\n1. 测试不存在的用户ID:")
    fake_uuid = "12345678-1234-1234-1234-123456789abc"
    try:
        response = requests.get(base_url, params={'user_id': fake_uuid})
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
    except Exception as e:
        print(f"  请求失败: {e}")
    
    # 2. 测试缺少用户ID
    print("\n2. 测试缺少用户ID:")
    try:
        response = requests.get(base_url)
        print(f"  状态码: {response.status_code}")
        print(f"  响应: {response.json()}")
    except Exception as e:
        print(f"  请求失败: {e}")
    
    # 3. 测试有效用户ID但没有日记数据
    print("\n3. 测试有效用户ID但没有日记数据:")
    try:
        # 获取一个没有日记的用户
        profile_no_diary = UserProfile.objects.filter(
            user__emotion_diaries__isnull=True
        ).first()
        
        if profile_no_diary:
            user_id = str(profile_no_diary.external_user_id)
            print(f"  测试用户: {profile_no_diary.user.username} ({user_id})")
            
            response = requests.get(base_url, params={'user_id': user_id})
            print(f"  状态码: {response.status_code}")
            print(f"  响应: {response.json()}")
        else:
            print("  没有找到无日记数据的用户")
    except Exception as e:
        print(f"  请求失败: {e}")
    
    # 4. 测试有效用户ID且有日记数据
    print("\n4. 测试有效用户ID且有日记数据:")
    try:
        # 获取一个有日记的用户
        profile_with_diary = UserProfile.objects.filter(
            user__emotion_diaries__isnull=False
        ).first()
        
        if profile_with_diary:
            user_id = str(profile_with_diary.external_user_id)
            print(f"  测试用户: {profile_with_diary.user.username} ({user_id})")
            
            response = requests.get(base_url, params={'user_id': user_id})
            print(f"  状态码: {response.status_code}")
            data = response.json()
            print(f"  成功: {data.get('success')}")
            print(f"  趋势数据条数: {len(data.get('trend_data', []))}")
            print(f"  总天数: {data.get('total_days')}")
        else:
            print("  没有找到有日记数据的用户")
    except Exception as e:
        print(f"  请求失败: {e}")

if __name__ == '__main__':
    test_trend_api_fix()

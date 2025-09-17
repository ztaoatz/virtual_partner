#!/usr/bin/env python
import os
import django
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from users.models import UserProfile
from lingxiapp.models import ChatSession, ChatMessage, EmotionDiary

def debug_trend_issue():
    print("=== 调试趋势图用户认证问题 ===")
    
    # 1. 检查所有UserProfile
    print(f"\n1. 数据库中所有用户资料:")
    profiles = UserProfile.objects.all()
    for profile in profiles:
        print(f"  - 用户: {profile.user.username}")
        print(f"    Django ID: {profile.user.id}")
        print(f"    External ID: {profile.external_user_id}")
        print(f"    昵称: {profile.nickname}")
        
        # 检查该用户的情绪日记
        diaries = EmotionDiary.objects.filter(user=profile.user)
        print(f"    情绪日记数量: {diaries.count()}")
        if diaries.exists():
            print(f"    最新日记: {diaries.last().date}")
        print()
    
    # 2. 模拟前端请求，测试问题
    print(f"\n2. 模拟问题场景:")
    
    # 假设前端传递了一个不存在的UUID
    fake_uuid = "12345678-1234-1234-1234-123456789abc"
    print(f"  测试UUID: {fake_uuid}")
    
    try:
        profile = UserProfile.objects.get(external_user_id=fake_uuid)
        print(f"  ✓ 找到用户: {profile.user.username}")
    except UserProfile.DoesNotExist:
        print(f"  ❌ 用户不存在 - 这就是错误原因!")
    
    # 3. 检查是否有临时用户的UUID格式问题
    print(f"\n3. 检查UUID格式问题:")
    import uuid
    
    # 生成一个正确的UUID格式
    valid_uuid = str(uuid.uuid4())
    print(f"  有效UUID示例: {valid_uuid}")
    
    # 检查数据库中的external_user_id是否都是有效的UUID格式
    for profile in profiles:
        try:
            uuid.UUID(str(profile.external_user_id))
            print(f"  ✓ {profile.user.username} 的UUID格式正确")
        except ValueError:
            print(f"  ❌ {profile.user.username} 的UUID格式错误: {profile.external_user_id}")

if __name__ == '__main__':
    debug_trend_issue()

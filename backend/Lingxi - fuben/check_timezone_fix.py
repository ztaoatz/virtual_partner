#!/usr/bin/env python
import os
import django
import sys
from datetime import datetime
import pytz

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.utils import timezone
from django.conf import settings
from lingxiapp.models import ChatMessage

def check_timezone_fix():
    """检查时区修复效果"""
    print("=== 时区设置检查 ===")
    
    # 1. 检查Django设置
    print(f"1. Django时区设置:")
    print(f"   TIME_ZONE: {settings.TIME_ZONE}")
    print(f"   USE_TZ: {settings.USE_TZ}")
    print(f"   LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
    
    # 2. 检查当前时间
    print(f"\n2. 时间对比:")
    
    # 系统时间
    system_now = datetime.now()
    print(f"   系统本地时间: {system_now}")
    
    # UTC时间
    utc_now = datetime.utcnow()
    print(f"   UTC时间: {utc_now}")
    
    # Django timezone时间
    django_now = timezone.now()
    print(f"   Django时区时间: {django_now}")
    
    # 转换为本地时间显示
    local_time = timezone.localtime(django_now)
    print(f"   Django本地时间: {local_time}")
    
    # 3. 检查上海时区
    shanghai_tz = pytz.timezone('Asia/Shanghai')
    shanghai_now = datetime.now(shanghai_tz)
    print(f"   上海时区时间: {shanghai_now}")
    
    # 4. 检查数据库中的最新消息时间
    print(f"\n3. 数据库消息时间检查:")
    latest_messages = ChatMessage.objects.order_by('-timestamp')[:3]
    
    for i, msg in enumerate(latest_messages, 1):
        # 原始时间戳
        original_time = msg.timestamp
        # 转换为本地时间
        local_time = timezone.localtime(original_time)
        
        print(f"   消息{i}: ")
        print(f"     原始时间戳: {original_time}")
        print(f"     本地时间: {local_time}")
        print(f"     用户: {msg.user.username}")
        print(f"     内容: {msg.content[:30]}...")
        print()
    
    # 5. 测试新消息的时间戳
    print(f"4. 如果现在创建新消息，时间戳会是:")
    test_time = timezone.now()
    test_local = timezone.localtime(test_time)
    print(f"   Django时间: {test_time}")
    print(f"   本地显示: {test_local}")
    
    # 6. 时区偏移检查
    print(f"\n5. 时区偏移信息:")
    current_offset = test_local.utcoffset()
    print(f"   UTC偏移: {current_offset}")
    print(f"   时区名称: {test_local.tzinfo.tzname(test_local)}")

if __name__ == '__main__':
    check_timezone_fix()

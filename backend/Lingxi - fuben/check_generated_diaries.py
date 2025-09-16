#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from lingxiapp.models import EmotionDiary
import json

print("=== 检查生成的情绪日记 ===")

diaries = EmotionDiary.objects.all().order_by('-created_at')
print(f"日记总数: {diaries.count()}")

for diary in diaries:
    print(f"\n--- 日记 ID: {diary.diary_id} ---")
    print(f"用户: {diary.user.username}")
    print(f"日期: {diary.date}")
    print(f"主要话题: {diary.main_topic}")
    print(f"消息数量: {diary.message_count}")
    print(f"创建时间: {diary.created_at}")
    
    # 解析情绪数据
    try:
        emotions = json.loads(diary.emotions) if diary.emotions else []
        print(f"情绪分析: {emotions}")
    except:
        print(f"情绪数据: {diary.emotions}")
    
    # 显示日记内容的前200字符
    content_preview = diary.content[:200] + "..." if len(diary.content) > 200 else diary.content
    print(f"内容预览: {content_preview}")

print("\n=== 检查完成 ===")

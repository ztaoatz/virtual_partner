#!/usr/bin/env python
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.contrib.auth.models import User
from users.models import UserProfile
import uuid

print("=== 修复缺失的UserProfile ===")

# 查找没有UserProfile的用户
users_without_profile = []
for user in User.objects.all():
    try:
        UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        users_without_profile.append(user)

print(f"发现 {len(users_without_profile)} 个用户没有UserProfile:")

for user in users_without_profile:
    external_user_id = str(uuid.uuid4())
    profile = UserProfile.objects.create(
        user=user,
        nickname=user.username if user.username else f'用户{user.id}',
        external_user_id=external_user_id
    )
    print(f"  为用户 {user.id} ({user.username}) 创建了UserProfile，external_user_id: {external_user_id}")

print("\n=== 修复完成，重新检查数据库 ===")

# 重新检查
profiles = UserProfile.objects.all()
print(f"\n用户资料表 (UserProfile) - 总数: {profiles.count()}")
for profile in profiles:
    print(f"  资料ID: {profile.id}, 用户ID: {profile.user.id}, 外部ID: {profile.external_user_id}, 昵称: {profile.nickname}")

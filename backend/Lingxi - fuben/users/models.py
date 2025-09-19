from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import uuid
import random
import string

# 用户扩展模型
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    external_user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nickname = models.CharField(max_length=50, default='用户')
    avatar_url = models.URLField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)  # 邮箱是否已验证
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nickname}({self.user.username})"

# 邮件验证码模型
class EmailVerification(models.Model):
    VERIFICATION_TYPES = [
        ('register', '注册验证'),
        ('password_reset', '密码重置'),
        ('email_change', '邮箱更改'),
    ]
    
    email = models.EmailField()
    code = models.CharField(max_length=10)
    verification_type = models.CharField(max_length=20, choices=VERIFICATION_TYPES, default='register')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # 关联用户（可选）
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            # 验证码5分钟后过期
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def generate_code(self):
        """生成6位数字验证码"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """检查验证码是否过期"""
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """检查验证码是否有效（未过期且未使用）"""
        return not self.is_expired() and not self.is_used
    
    def mark_as_used(self):
        """标记验证码为已使用"""
        self.is_used = True
        self.save()
    
    def __str__(self):
        return f"{self.email} - {self.code} ({self.verification_type})"

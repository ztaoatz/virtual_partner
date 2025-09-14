from django.db import models
from django.contrib.auth.models import User
import uuid

# 用户扩展模型
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    external_user_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    nickname = models.CharField(max_length=50, default='用户')
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nickname}({self.user.username})"

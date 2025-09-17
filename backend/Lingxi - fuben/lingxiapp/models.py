from django.db import models
from django.contrib.auth.models import User
import uuid

# 聊天会话模型
class ChatSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    title = models.CharField(max_length=100, default='新对话')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

# 聊天消息模型
class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', '用户消息'),
        ('ai', 'AI回复'),
        ('system', '系统消息'),
    ]
    
    message_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # 可选的元数据字段
    emotion = models.CharField(max_length=20, blank=True, null=True)  # 情绪标签
    confidence = models.FloatField(blank=True, null=True)  # AI回复的置信度
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.session.title} - {self.message_type}: {self.content[:50]}..."

# 用户偏好设置模型
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')
    ai_personality = models.CharField(max_length=50, default='友善助手')
    voice_enabled = models.BooleanField(default=True)
    auto_save_chat = models.BooleanField(default=True)
    max_chat_history = models.IntegerField(default=20)
    theme = models.CharField(max_length=20, default='default')
    
    def __str__(self):
        return f"{self.user.username}的偏好设置"

# 情绪日记模型
class EmotionDiary(models.Model):
    diary_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emotion_diaries')
    date = models.DateField()  # 日记对应的日期
    content = models.TextField()  # AI生成的日记内容
    emotions = models.TextField(blank=True, null=True)  # JSON格式的情绪分析结果
    main_topic = models.CharField(max_length=50, blank=True, null=True)  # 主要话题
    message_count = models.IntegerField(default=0)  # 该日期的消息数量
    emotion_score = models.FloatField(default=0.0)  # 当日情绪分值
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'date')  # 每个用户每天只能有一篇日记
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} 的情绪日记"

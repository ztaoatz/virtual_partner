from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import EmailVerification
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """邮件服务类"""
    
    @staticmethod
    def send_verification_code(email, verification_type='register', user=None):
        """
        发送验证码邮件
        
        Args:
            email: 目标邮箱
            verification_type: 验证类型 ('register', 'password_reset', 'email_change')
            user: 关联用户（可选）
        
        Returns:
            dict: 包含成功状态和验证码记录ID
        """
        try:
            # 创建验证码记录
            verification = EmailVerification.objects.create(
                email=email,
                verification_type=verification_type,
                user=user
            )
            
            # 根据验证类型设置邮件内容
            subject_mapping = {
                'register': '虚拟伴侣 - 注册验证码',
                'password_reset': '虚拟伴侣 - 密码重置验证码',
                'email_change': '虚拟伴侣 - 邮箱更改验证码'
            }
            
            template_mapping = {
                'register': 'email/register_verification.html',
                'password_reset': 'email/password_reset_verification.html', 
                'email_change': 'email/email_change_verification.html'
            }
            
            subject = subject_mapping.get(verification_type, '虚拟伴侣 - 验证码')
            
            # 准备邮件内容上下文
            context = {
                'code': verification.code,
                'email': email,
                'expires_minutes': 5,
                'verification_type': verification_type,
                'user': user,
                'site_name': '虚拟伴侣'
            }
            
            # 渲染邮件模板
            template_name = template_mapping.get(verification_type, 'email/default_verification.html')
            
            # 简单的HTML邮件内容（如果没有模板）
            html_message = f'''
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center;">
                    <h1 style="color: white; margin: 0;">虚拟伴侣</h1>
                </div>
                
                <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin-top: 20px;">
                    <h2 style="color: #333; margin-top: 0;">邮箱验证</h2>
                    <p style="color: #666; font-size: 16px; line-height: 1.6;">
                        您好！您正在进行邮箱验证，请使用以下验证码：
                    </p>
                    
                    <div style="background: white; border: 2px solid #667eea; border-radius: 8px; 
                               padding: 20px; margin: 25px 0; text-align: center;">
                        <span style="font-size: 32px; font-weight: bold; color: #667eea; 
                                    letter-spacing: 5px;">{verification.code}</span>
                    </div>
                    
                    <p style="color: #666; font-size: 14px;">
                        验证码将在 <strong>5分钟</strong> 后过期，请尽快使用。
                    </p>
                    
                    <p style="color: #999; font-size: 12px; margin-top: 30px;">
                        如果您没有请求此验证码，请忽略此邮件。
                    </p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
                    <p>此邮件由 虚拟伴侣 系统自动发送，请勿回复。</p>
                </div>
            </body>
            </html>
            '''
            
            # 纯文本版本
            plain_message = f'''
虚拟伴侣 - 邮箱验证

您好！

您正在进行邮箱验证，验证码为：{verification.code}

验证码将在5分钟后过期，请尽快使用。

如果您没有请求此验证码，请忽略此邮件。

此邮件由虚拟伴侣系统自动发送，请勿回复。
            '''
            
            # 发送邮件
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            logger.info(f"验证码邮件发送成功: {email}, 类型: {verification_type}")
            
            return {
                'success': True,
                'verification_id': verification.id,
                'message': '验证码发送成功'
            }
            
        except Exception as e:
            logger.error(f"发送验证码邮件失败: {email}, 错误: {str(e)}")
            return {
                'success': False,
                'error': f'邮件发送失败: {str(e)}'
            }
    
    @staticmethod
    def verify_code(email, code, verification_type='register'):
        """
        验证邮箱验证码
        
        Args:
            email: 邮箱地址
            code: 验证码
            verification_type: 验证类型
            
        Returns:
            dict: 验证结果
        """
        try:
            # 查找最新的有效验证码
            verification = EmailVerification.objects.filter(
                email=email,
                code=code,
                verification_type=verification_type,
                is_used=False
            ).order_by('-created_at').first()
            
            if not verification:
                return {
                    'success': False,
                    'error': '验证码不存在或已失效'
                }
            
            if verification.is_expired():
                return {
                    'success': False,
                    'error': '验证码已过期，请重新获取'
                }
            
            # 标记验证码为已使用
            verification.mark_as_used()
            
            logger.info(f"邮箱验证成功: {email}, 类型: {verification_type}")
            
            return {
                'success': True,
                'verification': verification,
                'message': '验证成功'
            }
            
        except Exception as e:
            logger.error(f"验证失败: {email}, 错误: {str(e)}")
            return {
                'success': False,
                'error': f'验证失败: {str(e)}'
            }
    
    @staticmethod
    def clean_expired_codes():
        """清理过期的验证码"""
        try:
            from django.utils import timezone
            expired_count = EmailVerification.objects.filter(
                expires_at__lt=timezone.now()
            ).delete()[0]
            
            logger.info(f"清理了 {expired_count} 个过期验证码")
            return expired_count
            
        except Exception as e:
            logger.error(f"清理过期验证码失败: {str(e)}")
            return 0

#!/usr/bin/env python
"""
邮件配置测试脚本
用于测试不同邮件服务提供商的配置
"""

import os
import django
import sys

# 添加Django项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_email_configuration():
    """测试邮件配置"""
    print("🧪 邮件配置测试")
    print("=" * 50)
    
    # 显示当前配置
    print("当前邮件配置:")
    print(f"  EMAIL_BACKEND: {getattr(settings, 'EMAIL_BACKEND', '未配置')}")
    print(f"  EMAIL_HOST: {getattr(settings, 'EMAIL_HOST', '未配置')}")
    print(f"  EMAIL_PORT: {getattr(settings, 'EMAIL_PORT', '未配置')}")
    print(f"  EMAIL_USE_TLS: {getattr(settings, 'EMAIL_USE_TLS', '未配置')}")
    print(f"  EMAIL_USE_SSL: {getattr(settings, 'EMAIL_USE_SSL', '未配置')}")
    print(f"  EMAIL_HOST_USER: {getattr(settings, 'EMAIL_HOST_USER', '未配置')}")
    print(f"  DEFAULT_FROM_EMAIL: {getattr(settings, 'DEFAULT_FROM_EMAIL', '未配置')}")
    print()
    
    # 检查必要配置
    required_settings = [
        'EMAIL_HOST',
        'EMAIL_HOST_USER', 
        'EMAIL_HOST_PASSWORD',
        'DEFAULT_FROM_EMAIL'
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
    
    if missing_settings:
        print("❌ 缺少必要配置:")
        for setting in missing_settings:
            print(f"  - {setting}")
        print("\n请参考邮件服务配置指南完成配置。")
        return False
    
    print("✅ 配置检查通过")
    return True

def test_send_email(recipient_email):
    """测试发送邮件"""
    print(f"\n📧 测试发送邮件到: {recipient_email}")
    
    try:
        subject = "虚拟伴侣系统 - 邮件测试"
        message = """
这是一封测试邮件，用于验证虚拟伴侣系统的邮件配置。

如果您收到这封邮件，说明邮件服务配置成功！

系统功能：
- 用户注册邮箱验证
- 密码重置功能
- 邮箱更改验证

此邮件由虚拟伴侣系统自动发送，请勿回复。
        """
        
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center;">
                <h1 style="color: white; margin: 0;">虚拟伴侣系统</h1>
                <p style="color: white; margin: 10px 0 0 0;">邮件配置测试</p>
            </div>
            
            <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin-top: 20px;">
                <h2 style="color: #333; margin-top: 0;">✅ 配置成功！</h2>
                <p style="color: #666; font-size: 16px; line-height: 1.6;">
                    恭喜！如果您收到这封邮件，说明虚拟伴侣系统的邮件服务配置成功。
                </p>
                
                <div style="background: white; border-left: 4px solid #667eea; padding: 15px; margin: 20px 0;">
                    <h3 style="color: #333; margin-top: 0;">系统功能</h3>
                    <ul style="color: #666;">
                        <li>用户注册邮箱验证</li>
                        <li>密码重置功能</li>
                        <li>邮箱更改验证</li>
                    </ul>
                </div>
                
                <p style="color: #666; font-size: 14px;">
                    现在您可以正常使用系统的邮件验证功能了。
                </p>
            </div>
            
            <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
                <p>此邮件由虚拟伴侣系统自动发送，请勿回复。</p>
            </div>
        </body>
        </html>
        """
        
        result = send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_message,
            fail_silently=False
        )
        
        if result:
            print("✅ 邮件发送成功！")
            print("请检查收件箱（包括垃圾邮件文件夹）")
            return True
        else:
            print("❌ 邮件发送失败：未知错误")
            return False
            
    except Exception as e:
        print(f"❌ 邮件发送失败: {str(e)}")
        logger.error(f"邮件发送错误: {str(e)}")
        return False

def main():
    """主函数"""
    print("虚拟伴侣系统 - 邮件配置测试工具")
    print("=" * 50)
    
    # 检查配置
    if not test_email_configuration():
        print("\n请先完成邮件服务配置，参考：邮件服务配置指南.md")
        return
    
    # 获取测试邮箱
    test_email = input("\n请输入用于测试的邮箱地址: ").strip()
    
    if not test_email:
        print("❌ 邮箱地址不能为空")
        return
    
    # 简单的邮箱格式验证
    if '@' not in test_email or '.' not in test_email:
        print("❌ 邮箱格式不正确")
        return
    
    # 发送测试邮件
    success = test_send_email(test_email)
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 邮件配置测试完成！系统已准备就绪。")
        print("\n接下来您可以：")
        print("1. 启动Django服务器")
        print("2. 启动前端应用")
        print("3. 测试用户注册功能")
        print("4. 测试密码重置功能")
    else:
        print("❌ 邮件配置测试失败。")
        print("\n请检查：")
        print("1. 邮件服务器配置是否正确")
        print("2. 网络连接是否正常")
        print("3. 邮箱授权码是否有效")
        print("4. 查看详细错误日志")

if __name__ == "__main__":
    main()

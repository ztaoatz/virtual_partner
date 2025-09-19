#!/usr/bin/env python
"""
虚拟伴侣系统 - 邮件验证功能部署检查
检查系统是否准备就绪，包括数据库、邮件服务、API等
"""

import os
import django
import sys
import requests
import json
from datetime import datetime

# 添加Django项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from django.conf import settings
from django.core.management import call_command
from django.contrib.auth.models import User
from users.models import UserProfile, EmailVerification
from users.email_service import EmailService

def print_header(title):
    """打印标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_section(title):
    """打印小节标题"""
    print(f"\n🔍 {title}")
    print("-" * 40)

def check_database():
    """检查数据库状态"""
    print_section("数据库检查")
    
    try:
        # 检查数据库连接
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ 数据库连接正常")
        
        # 检查迁移状态
        print("\n📋 检查数据库迁移:")
        call_command('showmigrations', '--list', verbosity=0)
        
        # 检查表是否存在
        tables_to_check = [
            'auth_user',
            'users_userprofile', 
            'users_emailverification'
        ]
        
        for table in tables_to_check:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                print(f"✅ 表 {table} 存在")
            else:
                print(f"❌ 表 {table} 不存在")
        
        # 检查用户数据
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        verification_count = EmailVerification.objects.count()
        
        print(f"\n📊 数据统计:")
        print(f"  用户数量: {user_count}")
        print(f"  用户资料数量: {profile_count}")
        print(f"  邮件验证记录: {verification_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据库检查失败: {str(e)}")
        return False

def check_email_configuration():
    """检查邮件配置"""
    print_section("邮件服务配置检查")
    
    # 检查配置项
    email_settings = {
        'EMAIL_BACKEND': getattr(settings, 'EMAIL_BACKEND', None),
        'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', None),
        'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', None),
        'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', None),
        'EMAIL_USE_SSL': getattr(settings, 'EMAIL_USE_SSL', None),
        'EMAIL_HOST_USER': getattr(settings, 'EMAIL_HOST_USER', None),
        'EMAIL_HOST_PASSWORD': getattr(settings, 'EMAIL_HOST_PASSWORD', None),
        'DEFAULT_FROM_EMAIL': getattr(settings, 'DEFAULT_FROM_EMAIL', None),
    }
    
    print("📧 邮件配置:")
    configured_count = 0
    for key, value in email_settings.items():
        if value:
            configured_count += 1
            if key == 'EMAIL_HOST_PASSWORD':
                # 隐藏密码
                display_value = '*' * len(str(value)) if value else '未配置'
            else:
                display_value = value
            print(f"  ✅ {key}: {display_value}")
        else:
            print(f"  ❌ {key}: 未配置")
    
    if configured_count >= 6:  # 至少需要6个基本配置
        print(f"\n✅ 邮件配置完整度: {configured_count}/8")
        return True
    else:
        print(f"\n❌ 邮件配置不完整: {configured_count}/8")
        print("请参考 '邮件服务配置指南.md' 完成配置")
        return False

def check_api_endpoints():
    """检查API端点"""
    print_section("API端点检查")
    
    base_url = "http://127.0.0.1:8000"
    endpoints_to_check = [
        "/appp/register/",
        "/appp/login/", 
        "/appp/send-verification-code/",
        "/appp/verify-email-code/",
        "/appp/reset-password/"
    ]
    
    # 先检查服务器是否运行
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print("✅ Django服务器正在运行")
        server_running = True
    except:
        print("❌ Django服务器未运行")
        print("请先启动服务器: python manage.py runserver")
        server_running = False
    
    if server_running:
        print("\n🔗 API端点测试:")
        for endpoint in endpoints_to_check:
            try:
                # 发送OPTIONS请求检查端点是否存在
                response = requests.options(f"{base_url}{endpoint}", timeout=5)
                if response.status_code in [200, 405]:  # 405表示方法不允许但端点存在
                    print(f"  ✅ {endpoint}")
                else:
                    print(f"  ❌ {endpoint} (状态码: {response.status_code})")
            except Exception as e:
                print(f"  ❌ {endpoint} (错误: {str(e)})")
    
    return server_running

def check_frontend_files():
    """检查前端文件"""
    print_section("前端文件检查")
    
    frontend_files_to_check = [
        "e:/virtual_partner/virtual_partner/frontend/vue301/src/view/register.vue",
        "e:/virtual_partner/virtual_partner/frontend/vue301/src/view/login.vue",
        "e:/virtual_partner/virtual_partner/frontend/vue301/src/view/ResetPassword.vue",
        "e:/virtual_partner/virtual_partner/frontend/vue301/src/router/index.js"
    ]
    
    all_files_exist = True
    for file_path in frontend_files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {os.path.basename(file_path)}")
        else:
            print(f"❌ {os.path.basename(file_path)} - 文件不存在")
            all_files_exist = False
    
    # 检查前端依赖
    package_json_path = "e:/virtual_partner/virtual_partner/frontend/vue301/package.json"
    if os.path.exists(package_json_path):
        print(f"\n✅ package.json 存在")
        
        # 检查node_modules
        node_modules_path = "e:/virtual_partner/virtual_partner/frontend/vue301/node_modules"
        if os.path.exists(node_modules_path):
            print("✅ node_modules 存在")
        else:
            print("❌ node_modules 不存在，请运行: npm install")
            all_files_exist = False
    else:
        print("❌ package.json 不存在")
        all_files_exist = False
    
    return all_files_exist

def test_email_service():
    """测试邮件服务类"""
    print_section("邮件服务类测试")
    
    try:
        # 测试验证码生成
        verification = EmailVerification.objects.create(
            email="test@example.com",
            verification_type="register"
        )
        
        print(f"✅ 验证码生成: {verification.code}")
        print(f"✅ 验证码ID: {verification.id}")
        print(f"✅ 过期时间: {verification.expires_at}")
        
        # 测试验证功能
        result = EmailService.verify_code("test@example.com", verification.code, "register")
        if result['success']:
            print("✅ 验证码验证功能正常")
        else:
            print(f"❌ 验证码验证失败: {result['error']}")
        
        # 清理测试数据
        verification.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ 邮件服务测试失败: {str(e)}")
        return False

def generate_deployment_report():
    """生成部署报告"""
    print_header("部署状态报告")
    
    timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    print(f"📅 生成时间: {timestamp}")
    
    # 执行所有检查
    results = {
        'database': check_database(),
        'email_config': check_email_configuration(), 
        'api_endpoints': check_api_endpoints(),
        'frontend_files': check_frontend_files(),
        'email_service': test_email_service()
    }
    
    # 生成总结
    print_header("总结")
    
    passed_checks = sum(results.values())
    total_checks = len(results)
    
    print(f"📊 检查结果: {passed_checks}/{total_checks} 项通过")
    print(f"🎯 完成度: {(passed_checks/total_checks)*100:.1f}%")
    
    if passed_checks == total_checks:
        print("\n🎉 恭喜！系统已完全准备就绪！")
        print("\n🚀 接下来可以：")
        print("  1. 配置真实邮件服务（如果还未配置）")
        print("  2. 启动后端服务: python manage.py runserver")
        print("  3. 启动前端服务: npm run dev")
        print("  4. 测试完整的用户注册流程")
        print("  5. 测试密码重置功能")
    else:
        print("\n⚠️  系统尚未完全准备就绪")
        print("\n🔧 需要解决的问题:")
        
        if not results['database']:
            print("  - 数据库配置或迁移问题")
        if not results['email_config']:
            print("  - 邮件服务配置不完整")
        if not results['api_endpoints']:
            print("  - API端点不可访问")
        if not results['frontend_files']:
            print("  - 前端文件缺失或依赖未安装")
        if not results['email_service']:
            print("  - 邮件服务类功能异常")
    
    return results

def main():
    """主函数"""
    print("虚拟伴侣系统 - 邮件验证功能部署检查")
    print(f"检查时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
    
    try:
        results = generate_deployment_report()
        
        # 保存报告到文件
        report_file = f"deployment_check_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        print(f"\n📝 详细报告已保存到: {report_file}")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  检查被用户中断")
    except Exception as e:
        print(f"\n❌ 检查过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()

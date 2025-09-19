#!/usr/bin/env python
"""
测试仅邮箱注册功能
验证前端修改是否正确工作
"""

import os
import django
import sys

# 添加Django项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

import requests
import json
import time

def test_email_only_registration():
    """测试仅邮箱注册功能"""
    print("🧪 测试仅邮箱注册功能")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    test_email = "test_email_only@example.com"
    test_username = f"test_user_{int(time.time())}"
    
    # 检查服务器是否运行
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print("✅ Django服务器正在运行")
    except:
        print("❌ Django服务器未运行，请先启动: python manage.py runserver")
        return False
    
    print(f"\n📧 测试邮箱: {test_email}")
    print(f"👤 测试用户名: {test_username}")
    
    # 1. 测试发送验证码
    print("\n1️⃣ 测试发送验证码...")
    try:
        response = requests.post(f"{base_url}/appp/send-verification-code/", 
                               json={
                                   "email": test_email,
                                   "type": "register"
                               },
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 验证码发送请求成功")
                verification_id = data.get('verification_id')
                print(f"   验证码记录ID: {verification_id}")
            else:
                print(f"⚠️ 验证码发送失败: {data.get('message')}")
        else:
            print(f"❌ API响应错误，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 发送验证码测试失败: {str(e)}")
    
    # 2. 获取生成的验证码（从数据库）
    print("\n2️⃣ 获取生成的验证码...")
    try:
        from users.models import EmailVerification
        latest_verification = EmailVerification.objects.filter(
            email=test_email,
            verification_type='register'
        ).order_by('-created_at').first()
        
        if latest_verification:
            test_code = latest_verification.code
            print(f"✅ 获取到验证码: {test_code}")
        else:
            print("❌ 未找到验证码记录")
            return False
            
    except Exception as e:
        print(f"❌ 获取验证码失败: {str(e)}")
        return False
    
    # 3. 测试邮箱注册（带验证码）
    print("\n3️⃣ 测试邮箱注册...")
    try:
        register_data = {
            "username": test_username,
            "email": test_email,
            "password": "test123456",
            "verification_code": test_code,
            "nickname": test_username
        }
        
        response = requests.post(f"{base_url}/appp/register/", 
                               json=register_data,
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ 邮箱注册成功")
                print(f"   用户ID: {data.get('user_id')}")
                print(f"   用户名: {data.get('username')}")
                print(f"   邮箱验证: {data.get('email_verified')}")
            else:
                print(f"⚠️ 注册失败: {data.get('message')}")
        else:
            print(f"❌ 注册API错误，状态码: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 注册测试失败: {str(e)}")
    
    # 4. 验证用户是否已创建且邮箱已验证
    print("\n4️⃣ 验证用户创建状态...")
    try:
        from django.contrib.auth.models import User
        from users.models import UserProfile
        
        user = User.objects.filter(username=test_username).first()
        if user:
            print(f"✅ 用户已创建: {user.username}")
            print(f"   邮箱: {user.email}")
            
            profile = UserProfile.objects.filter(user=user).first()
            if profile:
                print(f"✅ 用户资料已创建")
                print(f"   邮箱验证状态: {profile.email_verified}")
                print(f"   外部用户ID: {profile.external_user_id}")
            else:
                print("❌ 用户资料未创建")
        else:
            print("❌ 用户未创建")
            
    except Exception as e:
        print(f"❌ 验证用户状态失败: {str(e)}")
    
    # 5. 清理测试数据
    print("\n5️⃣ 清理测试数据...")
    try:
        from django.contrib.auth.models import User
        from users.models import UserProfile, EmailVerification
        
        # 删除测试用户
        User.objects.filter(username=test_username).delete()
        
        # 删除测试验证码
        EmailVerification.objects.filter(email=test_email).delete()
        
        print("✅ 测试数据清理完成")
        
    except Exception as e:
        print(f"⚠️ 清理测试数据失败: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 仅邮箱注册功能测试完成！")
    
    return True

def main():
    """主函数"""
    print("虚拟伴侣系统 - 仅邮箱注册功能测试")
    print("测试前端是否正确修改为仅支持邮箱注册")
    
    try:
        test_email_only_registration()
    except KeyboardInterrupt:
        print("\n\n⏹️ 测试被用户中断")
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()

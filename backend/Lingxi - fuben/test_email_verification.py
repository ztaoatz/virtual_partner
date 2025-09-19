#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件验证功能测试脚本
测试发送验证码和验证功能
"""

import os
import django
import requests
import json
import time

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
django.setup()

from users.email_service import EmailService
from users.models import EmailVerification

def test_email_service():
    """测试邮件服务类"""
    print("=== 测试邮件服务类 ===")
    
    test_email = "test@example.com"  # 替换为真实邮箱进行测试
    
    # 测试发送验证码
    print(f"发送验证码到: {test_email}")
    result = EmailService.send_verification_code(test_email, 'register')
    
    if result['success']:
        print(f"✅ 验证码发送成功")
        print(f"   验证记录ID: {result['verification_id']}")
        
        # 获取验证码用于测试
        verification = EmailVerification.objects.get(id=result['verification_id'])
        test_code = verification.code
        print(f"   生成的验证码: {test_code}")
        
        # 测试验证功能
        print(f"\n验证验证码...")
        verify_result = EmailService.verify_code(test_email, test_code, 'register')
        
        if verify_result['success']:
            print(f"✅ 验证码验证成功")
        else:
            print(f"❌ 验证码验证失败: {verify_result['error']}")
            
    else:
        print(f"❌ 验证码发送失败: {result['error']}")

def test_api_endpoints():
    """测试API接口"""
    print("\n=== 测试API接口 ===")
    
    base_url = "http://127.0.0.1:8000/appp"
    test_email = "test@example.com"  # 替换为真实邮箱
    
    # 1. 测试发送验证码接口
    print("1. 测试发送验证码接口")
    try:
        response = requests.post(f"{base_url}/send-verification-code/", 
                               json={
                                   'email': test_email,
                                   'type': 'register'
                               },
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ API发送验证码成功")
                print(f"   响应: {data['message']}")
                verification_id = data.get('verification_id')
                
                # 获取验证码进行后续测试
                if verification_id:
                    verification = EmailVerification.objects.get(id=verification_id)
                    test_code = verification.code
                    
                    # 2. 测试验证验证码接口
                    print(f"\n2. 测试验证验证码接口")
                    verify_response = requests.post(f"{base_url}/verify-email-code/",
                                                  json={
                                                      'email': test_email,
                                                      'code': test_code,
                                                      'type': 'register'
                                                  },
                                                  timeout=10)
                    
                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        if verify_data.get('success'):
                            print(f"✅ API验证验证码成功")
                        else:
                            print(f"❌ API验证验证码失败: {verify_data['message']}")
                    else:
                        print(f"❌ 验证接口请求失败: {verify_response.status_code}")
                        
            else:
                print(f"❌ API发送验证码失败: {data['message']}")
        else:
            print(f"❌ 发送验证码请求失败: {response.status_code}")
            print(f"   响应: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")

def test_registration_flow():
    """测试完整注册流程"""
    print("\n=== 测试完整注册流程 ===")
    
    base_url = "http://127.0.0.1:8000/appp"
    test_data = {
        'username': f'testuser_{int(time.time())}',
        'email': 'test@example.com',  # 替换为真实邮箱
        'password': 'testpass123',
        'nickname': '测试用户'
    }
    
    print(f"测试用户: {test_data['username']}")
    print(f"测试邮箱: {test_data['email']}")
    
    # 1. 发送验证码
    print("1. 发送注册验证码...")
    try:
        code_response = requests.post(f"{base_url}/send-verification-code/",
                                    json={
                                        'email': test_data['email'],
                                        'type': 'register'
                                    },
                                    timeout=10)
        
        if code_response.status_code == 200 and code_response.json().get('success'):
            verification_id = code_response.json()['verification_id']
            verification = EmailVerification.objects.get(id=verification_id)
            verification_code = verification.code
            
            print(f"✅ 验证码发送成功: {verification_code}")
            
            # 2. 使用验证码注册
            print("2. 使用验证码注册用户...")
            test_data['verification_code'] = verification_code
            
            register_response = requests.post(f"{base_url}/register/",
                                            json=test_data,
                                            timeout=10)
            
            if register_response.status_code == 200:
                register_data = register_response.json()
                if register_data.get('success'):
                    print(f"✅ 用户注册成功")
                    print(f"   用户ID: {register_data['user_id']}")
                    print(f"   用户名: {register_data['username']}")
                    print(f"   邮箱验证: {register_data.get('email_verified', False)}")
                else:
                    print(f"❌ 用户注册失败: {register_data['message']}")
            else:
                print(f"❌ 注册请求失败: {register_response.status_code}")
                print(f"   响应: {register_response.text}")
                
        else:
            print(f"❌ 验证码发送失败")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")

def test_password_reset_flow():
    """测试密码重置流程"""
    print("\n=== 测试密码重置流程 ===")
    
    base_url = "http://127.0.0.1:8000/appp"
    test_email = "test@example.com"  # 需要是已注册的邮箱
    
    # 1. 发送密码重置验证码
    print("1. 发送密码重置验证码...")
    try:
        code_response = requests.post(f"{base_url}/send-verification-code/",
                                    json={
                                        'email': test_email,
                                        'type': 'password_reset'
                                    },
                                    timeout=10)
        
        if code_response.status_code == 200:
            code_data = code_response.json()
            if code_data.get('success'):
                print(f"✅ 密码重置验证码发送成功")
                
                # 获取验证码
                verification_id = code_data['verification_id']
                verification = EmailVerification.objects.get(id=verification_id)
                verification_code = verification.code
                
                print(f"   验证码: {verification_code}")
                
                # 2. 重置密码
                print("2. 重置密码...")
                reset_response = requests.post(f"{base_url}/reset-password/",
                                             json={
                                                 'email': test_email,
                                                 'verification_code': verification_code,
                                                 'new_password': 'newpassword123'
                                             },
                                             timeout=10)
                
                if reset_response.status_code == 200:
                    reset_data = reset_response.json()
                    if reset_data.get('success'):
                        print(f"✅ 密码重置成功")
                    else:
                        print(f"❌ 密码重置失败: {reset_data['message']}")
                else:
                    print(f"❌ 密码重置请求失败: {reset_response.status_code}")
                    
            else:
                print(f"❌ 验证码发送失败: {code_data['message']}")
        else:
            print(f"❌ 验证码发送请求失败: {code_response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")

def test_database_cleanup():
    """测试数据库清理功能"""
    print("\n=== 测试数据库清理功能 ===")
    
    # 清理过期验证码
    cleaned_count = EmailService.clean_expired_codes()
    print(f"清理过期验证码数量: {cleaned_count}")
    
    # 显示当前验证码统计
    total_codes = EmailVerification.objects.count()
    active_codes = EmailVerification.objects.filter(is_used=False).count()
    
    print(f"验证码总数: {total_codes}")
    print(f"未使用验证码: {active_codes}")

def main():
    """主测试函数"""
    print("🧪 邮件验证功能测试开始")
    print("=" * 50)
    
    # 注意：在实际测试前，请确保：
    # 1. Django服务器正在运行 (python manage.py runserver)
    # 2. 邮件配置已正确设置
    # 3. 测试邮箱地址替换为真实邮箱
    
    try:
        # 测试邮件服务类
        test_email_service()
        
        # 测试API接口
        test_api_endpoints()
        
        # 测试完整注册流程
        test_registration_flow()
        
        # 测试密码重置流程
        # test_password_reset_flow()  # 需要已注册的邮箱
        
        # 测试数据库清理
        test_database_cleanup()
        
        print("\n" + "=" * 50)
        print("✅ 邮件验证功能测试完成")
        
    except Exception as e:
        print(f"\n❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

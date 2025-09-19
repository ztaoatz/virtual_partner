#!/usr/bin/env python
"""
虚拟伴侣系统 - 快速启动和测试脚本
一键测试邮件验证功能的完整性
"""

import os
import sys
import time
import subprocess
import threading
import requests
import json
from datetime import datetime

def print_banner():
    """打印启动横幅"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    虚拟伴侣系统                               ║
    ║                   邮件验证功能测试                             ║
    ║                                                              ║
    ║                  🚀 快速启动向导 🚀                           ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_prerequisites():
    """检查先决条件"""
    print("🔍 检查系统先决条件...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 8:
        print(f"✅ Python版本: {python_version.major}.{python_version.minor}")
    else:
        print(f"❌ Python版本过低: {python_version.major}.{python_version.minor}")
        return False
    
    # 检查Django是否安装
    try:
        import django
        print(f"✅ Django版本: {django.get_version()}")
    except ImportError:
        print("❌ Django未安装，请运行: pip install django")
        return False
    
    # 检查项目目录
    backend_path = "e:/virtual_partner/virtual_partner/backend/Lingxi - fuben"
    frontend_path = "e:/virtual_partner/virtual_partner/frontend/vue301"
    
    if os.path.exists(backend_path):
        print("✅ 后端项目目录存在")
    else:
        print(f"❌ 后端项目目录不存在: {backend_path}")
        return False
    
    if os.path.exists(frontend_path):
        print("✅ 前端项目目录存在")
    else:
        print(f"❌ 前端项目目录不存在: {frontend_path}")
        return False
    
    return True

def setup_django():
    """设置Django环境"""
    os.chdir("e:/virtual_partner/virtual_partner/backend/Lingxi - fuben")
    
    # 设置Django环境变量
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lingxi.settings')
    
    import django
    django.setup()
    
    print("✅ Django环境已设置")

def test_database():
    """测试数据库连接"""
    print("\n🗄️ 测试数据库连接...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        print("✅ 数据库连接正常")
        return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        return False

def start_django_server():
    """启动Django服务器"""
    print("\n🚀 启动Django服务器...")
    
    def run_server():
        os.chdir("e:/virtual_partner/virtual_partner/backend/Lingxi - fuben")
        subprocess.run([sys.executable, "manage.py", "runserver", "--verbosity=0"], 
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # 等待服务器启动
    for i in range(10):
        try:
            response = requests.get("http://127.0.0.1:8000/admin/", timeout=2)
            print("✅ Django服务器已启动")
            return True
        except:
            print(f"⏳ 等待服务器启动... ({i+1}/10)")
            time.sleep(2)
    
    print("❌ Django服务器启动失败")
    return False

def test_email_apis():
    """测试邮件相关API"""
    print("\n📧 测试邮件API...")
    
    base_url = "http://127.0.0.1:8000"
    
    # 测试发送验证码API
    print("  测试发送验证码API...")
    try:
        response = requests.post(f"{base_url}/appp/send-verification-code/", 
                               json={"email": "test@example.com", "type": "register"},
                               timeout=5)
        if response.status_code == 200:
            print("  ✅ 发送验证码API响应正常")
        else:
            print(f"  ⚠️ 发送验证码API状态码: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 发送验证码API测试失败: {str(e)}")
    
    # 测试验证码验证API
    print("  测试验证码验证API...")
    try:
        response = requests.post(f"{base_url}/appp/verify-email-code/", 
                               json={"email": "test@example.com", "code": "123456", "type": "register"},
                               timeout=5)
        if response.status_code == 200:
            print("  ✅ 验证码验证API响应正常")
        else:
            print(f"  ⚠️ 验证码验证API状态码: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 验证码验证API测试失败: {str(e)}")
    
    # 测试注册API
    print("  测试注册API...")
    try:
        response = requests.post(f"{base_url}/appp/register/", 
                               json={"username": "testuser", "password": "testpass123"},
                               timeout=5)
        if response.status_code == 200:
            print("  ✅ 注册API响应正常")
        else:
            print(f"  ⚠️ 注册API状态码: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 注册API测试失败: {str(e)}")

def check_frontend():
    """检查前端环境"""
    print("\n🎨 检查前端环境...")
    
    frontend_path = "e:/virtual_partner/virtual_partner/frontend/vue301"
    
    # 检查package.json
    package_json_path = os.path.join(frontend_path, "package.json")
    if os.path.exists(package_json_path):
        print("✅ package.json存在")
    else:
        print("❌ package.json不存在")
        return False
    
    # 检查node_modules
    node_modules_path = os.path.join(frontend_path, "node_modules")
    if os.path.exists(node_modules_path):
        print("✅ node_modules存在")
    else:
        print("❌ node_modules不存在，需要运行 npm install")
        return False
    
    # 检查关键文件
    key_files = [
        "src/view/register.vue",
        "src/view/login.vue", 
        "src/view/ResetPassword.vue",
        "src/router/index.js"
    ]
    
    for file_path in key_files:
        full_path = os.path.join(frontend_path, file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} 不存在")
            return False
    
    return True

def show_next_steps():
    """显示下一步操作"""
    print("\n" + "="*60)
    print("🎯 系统测试完成！")
    print("="*60)
    
    print("\n📋 接下来的步骤:")
    print("1. 📧 配置真实邮件服务")
    print("   - 编辑 backend/Lingxi - fuben/Lingxi/settings.py")
    print("   - 参考 '邮件服务配置指南.md'")
    print("   - 运行 python test_email_config.py 测试")
    
    print("\n2. 🚀 启动完整系统")
    print("   后端: python manage.py runserver")
    print("   前端: cd frontend/vue301 && npm run dev")
    
    print("\n3. 🧪 测试功能")
    print("   - 访问 http://localhost:3000")
    print("   - 测试邮箱注册功能")
    print("   - 测试密码重置功能")
    
    print("\n4. 📊 监控系统")
    print("   - 运行 python deployment_check.py")
    print("   - 查看系统状态报告")
    
    print("\n🎉 恭喜！您的虚拟伴侣系统已准备就绪！")

def main():
    """主函数"""
    try:
        print_banner()
        
        # 检查先决条件
        if not check_prerequisites():
            print("\n❌ 先决条件检查失败，请解决问题后重试")
            return
        
        # 设置Django环境
        setup_django()
        
        # 测试数据库
        if not test_database():
            print("\n❌ 数据库测试失败")
            return
        
        # 启动Django服务器
        if not start_django_server():
            print("\n❌ Django服务器启动失败")
            return
        
        # 测试API
        test_email_apis()
        
        # 检查前端
        frontend_ok = check_frontend()
        
        # 显示下一步
        show_next_steps()
        
        # 保持服务器运行
        print(f"\n⏰ Django服务器正在运行... (启动时间: {datetime.now().strftime('%H:%M:%S')})")
        print("💡 按 Ctrl+C 停止服务器")
        
        try:
            while True:
                time.sleep(60)
                print(f"📡 服务器运行中... {datetime.now().strftime('%H:%M:%S')}")
        except KeyboardInterrupt:
            print("\n\n⏹️  服务器已停止")
            
    except Exception as e:
        print(f"\n❌ 启动过程中发生错误: {str(e)}")

if __name__ == "__main__":
    main()

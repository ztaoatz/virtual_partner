#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ollama代理服务版本切换脚本
可以在原版本和优化版本之间切换
"""

import os
import shutil
import sys

def backup_current_version():
    """备份当前版本"""
    current_file = r'e:\virtual_partner\virtual_partner\ollama_proxy.py'
    backup_file = r'e:\virtual_partner\virtual_partner\ollama_proxy_backup.py'
    
    if os.path.exists(current_file):
        shutil.copy2(current_file, backup_file)
        print(f"✅ 已备份当前版本到: {backup_file}")
        return True
    else:
        print(f"❌ 当前版本文件不存在: {current_file}")
        return False

def switch_to_optimized():
    """切换到优化版本"""
    optimized_file = r'e:\virtual_partner\virtual_partner\ollama_proxy_optimized.py'
    current_file = r'e:\virtual_partner\virtual_partner\ollama_proxy.py'
    
    if not os.path.exists(optimized_file):
        print(f"❌ 优化版本文件不存在: {optimized_file}")
        return False
    
    # 备份当前版本
    backup_current_version()
    
    # 替换为优化版本
    shutil.copy2(optimized_file, current_file)
    print(f"✅ 已切换到优化版本")
    
    return True

def switch_to_original():
    """切换回原版本"""
    backup_file = r'e:\virtual_partner\virtual_partner\ollama_proxy_backup.py'
    current_file = r'e:\virtual_partner\virtual_partner\ollama_proxy.py'
    
    if not os.path.exists(backup_file):
        print(f"❌ 备份文件不存在: {backup_file}")
        return False
    
    # 恢复原版本
    shutil.copy2(backup_file, current_file)
    print(f"✅ 已切换回原版本")
    
    return True

def show_current_version_info():
    """显示当前版本信息"""
    current_file = r'e:\virtual_partner\virtual_partner\ollama_proxy.py'
    
    if not os.path.exists(current_file):
        print("❌ 当前版本文件不存在")
        return
    
    try:
        with open(current_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 检查版本标识
        if '优化版本' in content or 'optimized' in content:
            print("📋 当前版本: 优化版本")
            print("   特性: 重试机制、内容验证、增强错误处理")
        else:
            print("📋 当前版本: 原版本")
            print("   特性: 基础功能")
            
        # 显示文件大小和修改时间
        stat = os.stat(current_file)
        size = stat.st_size
        mtime = stat.st_mtime
        
        import datetime
        mod_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        print(f"   文件大小: {size} 字节")
        print(f"   修改时间: {mod_time}")
        
    except Exception as e:
        print(f"❌ 读取版本信息失败: {e}")

def main():
    """主函数"""
    print("🔄 Ollama代理服务版本切换工具")
    print("=" * 50)
    
    show_current_version_info()
    
    print("\n请选择操作:")
    print("1. 切换到优化版本 (重试机制、内容验证)")
    print("2. 切换回原版本")
    print("3. 显示版本信息")
    print("4. 退出")
    
    while True:
        choice = input("\n请输入选项 (1-4): ").strip()
        
        if choice == '1':
            print("\n🔄 正在切换到优化版本...")
            if switch_to_optimized():
                print("✅ 切换成功！")
                print("📌 重要提示:")
                print("   - 优化版本包含重试机制，最多尝试3次")
                print("   - 增加了内容质量验证")
                print("   - 改进了错误处理和超时设置")
                print("   - 建议重启Ollama代理服务以生效")
            break
            
        elif choice == '2':
            print("\n🔄 正在切换回原版本...")
            if switch_to_original():
                print("✅ 切换成功！")
                print("📌 已恢复到原版本")
                print("   - 建议重启Ollama代理服务以生效")
            break
            
        elif choice == '3':
            print("\n📋 版本信息:")
            show_current_version_info()
            
        elif choice == '4':
            print("👋 退出")
            break
            
        else:
            print("❌ 无效选项，请重新输入")

if __name__ == "__main__":
    main()

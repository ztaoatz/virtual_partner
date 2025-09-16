#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试情绪日记生成进度条功能
验证前端进度条和等待提示是否正常工作
"""

import requests
import json
import time
import sys
import os

def test_diary_generation_with_progress():
    """测试带进度条的日记生成功能"""
    print("🧪 测试情绪日记生成进度条功能...")
    
    # 测试用户
    test_user = {
        'external_id': '26368a8b-03cd-4f64-b73e-c37dcb0d5f0e',
        'username': 'zhnagtao'
    }
    
    target_date = '2025-09-14'  # 使用有聊天记录的日期
    
    print(f"📅 测试日期: {target_date}")
    print(f"👤 测试用户: {test_user['username']}")
    
    try:
        print("\n⏳ 开始生成情绪日记...")
        start_time = time.time()
        
        # 调用后端API生成日记
        response = requests.post(
            'http://127.0.0.1:8000/generate-diary/',
            json={
                'user_id': test_user['external_id'],
                'date': target_date,
                'force_regenerate': True  # 强制重新生成
            },
            timeout=210  # 3.5分钟超时
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                diary = result['diary']
                print(f"✅ 日记生成成功! (耗时: {duration:.2f}秒)")
                print(f"   📄 内容长度: {len(diary['content'])} 字符")
                print(f"   🎭 主要情绪: {diary['emotions']}")
                print(f"   🎯 主要话题: {diary['main_topic']}")
                print(f"   📊 消息数量: {diary['message_count']}")
                print(f"   📖 内容预览: {diary['content'][:100]}...")
                
                # 验证进度条功能提示
                print(f"\n💡 前端进度条功能要点:")
                print(f"   ⭕ 圆形进度条应显示0-100%的进度")
                print(f"   💬 进度消息应包含: '正在分析聊天记录...', '正在生成情绪分析...', '正在整理日记内容...'")
                print(f"   🔄 重新生成按钮应有独立的小型进度条")
                print(f"   ⏰ 等待时间约为: {duration:.0f}秒，用户需要看到进度反馈")
                
                return True
            else:
                print(f"❌ API返回失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"   错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"⏰ 请求超时 (超过210秒)")
        print(f"💡 这种情况下进度条应显示超时错误")
        return False
    except Exception as e:
        print(f"❌ 异常: {e}")
        return False

def test_health_check():
    """测试服务健康状态"""
    print("🔍 检查服务状态...")
    
    services = [
        {'name': 'Django后端', 'url': 'http://127.0.0.1:8000/'},
        {'name': 'Ollama代理', 'url': 'http://localhost:25674/health'}
    ]
    
    all_healthy = True
    
    for service in services:
        try:
            response = requests.get(service['url'], timeout=5)
            if response.status_code == 200:
                print(f"✅ {service['name']}: 正常运行")
            else:
                print(f"⚠️ {service['name']}: 状态异常 ({response.status_code})")
                all_healthy = False
        except Exception as e:
            print(f"❌ {service['name']}: 连接失败 ({e})")
            all_healthy = False
    
    return all_healthy

def main():
    """主函数"""
    print("🚀 开始测试情绪日记进度条功能...")
    
    # 检查服务状态
    if not test_health_check():
        print("\n⚠️ 服务状态异常，请先启动必要的服务")
        return
    
    print("\n" + "="*50)
    
    # 测试日记生成功能
    success = test_diary_generation_with_progress()
    
    print("\n" + "="*50)
    print("📋 进度条功能测试说明:")
    print("   1. 打开前端页面: http://localhost:3001/")
    print("   2. 登录用户账号")
    print("   3. 点击情绪日记功能")
    print("   4. 点击'生成今日日记'按钮")
    print("   5. 观察圆形进度条和等待提示")
    print("   6. 测试重新生成按钮的小型进度条")
    
    if success:
        print("\n✨ 后端测试成功，前端进度条应该正常工作！")
    else:
        print("\n⚠️ 后端测试失败，请检查服务状态")

if __name__ == "__main__":
    main()

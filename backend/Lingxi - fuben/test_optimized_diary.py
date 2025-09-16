#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试优化后的情绪日记生成功能
包括超时处理、重试机制和内容质量验证
"""

import requests
import json
import time
import sys
import os

# 添加项目路径
sys.path.append(r'e:\virtual_partner\virtual_partner\backend\Lingxi - fuben')

def test_diary_generation_optimized():
    """测试优化后的日记生成功能"""
    print("🧪 开始测试优化后的情绪日记生成功能...")
    
    # 测试用例：模拟真实聊天记录
    test_cases = [
        {
            "name": "正常长度聊天",
            "chat_history": [
                {"text": "今天工作压力好大，感觉有点焦虑", "isUser": True},
                {"text": "我理解你的感受，工作压力确实会让人感到焦虑。可以和我聊聊具体是什么让你感到压力吗？", "isUser": False},
                {"text": "主要是项目deadline快到了，但进度还不太理想", "isUser": True},
                {"text": "deadline压力确实很大。不过既然已经意识到问题，我们可以一起想想如何更好地安排剩余时间。", "isUser": False},
                {"text": "是的，我觉得需要重新规划一下任务优先级", "isUser": True},
                {"text": "很好的想法！制定清晰的优先级可以帮助你更有效地完成工作，也能减少焦虑感。", "isUser": False}
            ]
        },
        {
            "name": "短对话测试",
            "chat_history": [
                {"text": "今天心情不错", "isUser": True},
                {"text": "很高兴听到你心情好！有什么特别的事情让你开心吗？", "isUser": False},
                {"text": "和朋友一起吃了顿美食", "isUser": True}
            ]
        },
        {
            "name": "情绪复杂对话",
            "chat_history": [
                {"text": "最近总是感觉很迷茫，不知道未来要做什么", "isUser": True},
                {"text": "迷茫是很正常的情感体验，它说明你在思考和成长。可以先聊聊你现在最关心的是什么？", "isUser": False},
                {"text": "主要是职业发展方向，感觉现在的工作没什么意思", "isUser": True},
                {"text": "职业发展的困惑确实会让人感到不安。你觉得什么样的工作会让你感到有意义呢？", "isUser": False},
                {"text": "我希望能做一些帮助别人的工作，但又担心收入问题", "isUser": True},
                {"text": "你的想法很有意义！帮助他人确实能带来满足感。我们可以探讨一下如何在理想和现实之间找到平衡。", "isUser": False}
            ]
        }
    ]
    
    # 测试每个用例
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 测试用例 {i}: {test_case['name']}")
        print(f"   聊天记录数: {len(test_case['chat_history'])}")
        
        try:
            start_time = time.time()
            
            # 调用优化后的API
            response = requests.post(
                'http://localhost:25674/generate-diary/',
                json={
                    'chat_history': test_case['chat_history'],
                    'user_name': '测试用户',
                    'date': '2024-01-15'
                },
                timeout=150  # 2.5分钟超时
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    diary_content = result.get('diary_content', '')
                    emotions = result.get('emotions', [])
                    main_topic = result.get('main_topic', '')
                    
                    print(f"   ✅ 生成成功 (耗时: {duration:.2f}秒)")
                    print(f"   📄 日记长度: {len(diary_content)} 字符")
                    print(f"   🎭 主要情绪: {[e['emotion'] for e in emotions[:2]]}")
                    print(f"   🎯 主要话题: {main_topic}")
                    print(f"   📖 日记内容预览: {diary_content[:100]}...")
                    
                    # 验证内容质量
                    if len(diary_content) >= 100:
                        print(f"   ✅ 内容长度符合要求")
                        success_count += 1
                    else:
                        print(f"   ❌ 内容过短 ({len(diary_content)} 字符)")
                else:
                    print(f"   ❌ API返回失败: {result.get('error', '未知错误')}")
            else:
                print(f"   ❌ HTTP错误: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
        except requests.exceptions.Timeout:
            print(f"   ⏰ 请求超时 (超过150秒)")
        except Exception as e:
            print(f"   ❌ 异常: {e}")
        
        # 测试间隔
        if i < total_count:
            print("   ⏳ 等待5秒后继续下一个测试...")
            time.sleep(5)
    
    # 总结
    print(f"\n📊 测试总结:")
    print(f"   总测试数: {total_count}")
    print(f"   成功数: {success_count}")
    print(f"   成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 所有测试通过！优化效果良好。")
    elif success_count > total_count * 0.7:
        print("✅ 大部分测试通过，优化有效果。")
    else:
        print("⚠️  成功率较低，可能需要进一步优化。")

def test_health_check():
    """测试健康检查接口"""
    print("\n🔍 测试健康检查接口...")
    
    try:
        response = requests.get('http://localhost:25674/health', timeout=10)
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ 服务状态: {result.get('status')}")
            print(f"   🔗 Ollama连接: {result.get('ollama')}")
            models = result.get('available_models', [])
            print(f"   🤖 可用模型: {models}")
        else:
            print(f"   ❌ 健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"   ❌ 健康检查异常: {e}")

def main():
    """主函数"""
    print("🚀 开始测试优化后的Ollama代理服务...")
    
    # 首先测试健康状态
    test_health_check()
    
    # 然后测试日记生成功能
    test_diary_generation_optimized()
    
    print("\n✨ 测试完成！")

if __name__ == "__main__":
    main()

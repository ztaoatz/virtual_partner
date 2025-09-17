#!/usr/bin/env python
"""
TTS服务测试脚本
用于验证Nahida TTS服务是否正常工作
"""

import requests
import json
import pyaudio
import sys

def test_tts_direct():
    """直接测试TTS服务"""
    print("=== 直接测试TTS服务 (127.0.0.1:5000) ===")
    
    try:
        payload = {
            "cha_name": "nahida",
            "text": "你好，这是Nahida语音测试",
            "text_language": "多语种混合",
            "character_emotion": "default",
            "batch_size": 1,
            "stream": True
        }
        
        response = requests.post(
            "http://127.0.0.1:5000/tts", 
            json=payload, 
            stream=True,
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ TTS服务正常，音频数据获取成功")
            return True
        else:
            print(f"❌ TTS服务错误，状态码: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到TTS服务，请确保服务运行在 http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"❌ TTS服务测试异常: {e}")
        return False

def test_django_tts_api():
    """测试Django TTS API"""
    print("\n=== 测试Django TTS API (127.0.0.1:8000) ===")
    
    try:
        # 首先检查状态
        status_response = requests.get("http://127.0.0.1:8000/tts-status/", timeout=5)
        print(f"TTS状态检查: {status_response.json()}")
        
        # 测试TTS API
        tts_payload = {
            "text": "你好，这是通过Django API的Nahida语音测试"
        }
        
        tts_response = requests.post(
            "http://127.0.0.1:8000/nahida-tts/",
            json=tts_payload,
            timeout=15
        )
        
        if tts_response.status_code == 200:
            print("✅ Django TTS API正常，音频数据获取成功")
            print(f"响应Content-Type: {tts_response.headers.get('content-type')}")
            return True
        else:
            print(f"❌ Django TTS API错误，状态码: {tts_response.status_code}")
            if tts_response.headers.get('content-type') == 'application/json':
                print(f"错误信息: {tts_response.json()}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到Django服务，请确保Django运行在 http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Django TTS API测试异常: {e}")
        return False

def play_audio_test():
    """测试音频播放功能"""
    print("\n=== 测试音频播放功能 ===")
    
    try:
        payload = {
            "cha_name": "nahida",
            "text": "这是一个完整的音频播放测试",
            "text_language": "多语种混合",
            "character_emotion": "default",
            "batch_size": 1,
            "stream": True
        }

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=32000,
                        output=True,
                        frames_per_buffer=1024)

        print("🎵 开始播放音频...")
        resp = requests.post("http://127.0.0.1:5000/tts", json=payload, stream=True)
        
        if resp.status_code == 200:
            for chunk in resp.iter_content(chunk_size=1024):
                if chunk:
                    stream.write(chunk)
            print("✅ 音频播放完成")
        else:
            print(f"❌ 音频获取失败，状态码: {resp.status_code}")

        stream.stop_stream()
        stream.close()
        p.terminate()
        return True
        
    except ImportError:
        print("❌ pyaudio未安装，跳过音频播放测试")
        print("提示: 可以运行 pip install pyaudio 来安装")
        return False
    except Exception as e:
        print(f"❌ 音频播放测试异常: {e}")
        return False

def main():
    print("🎤 Nahida TTS服务全面测试")
    print("=" * 50)
    
    # 测试结果
    results = []
    
    # 1. 直接测试TTS服务
    results.append(("TTS服务", test_tts_direct()))
    
    # 2. 测试Django API
    results.append(("Django TTS API", test_django_tts_api()))
    
    # 3. 测试音频播放
    if "--with-audio" in sys.argv:
        results.append(("音频播放", play_audio_test()))
    else:
        print("\n💡 提示: 使用 --with-audio 参数来测试音频播放功能")
    
    # 输出测试结果总结
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    # 给出建议
    all_passed = all(result for _, result in results)
    if all_passed:
        print("\n🎉 所有测试通过！Nahida TTS服务可以正常使用")
    else:
        print("\n⚠️  部分测试失败，请检查相关服务:")
        print("  1. 确保TTS服务运行在 http://127.0.0.1:5000")
        print("  2. 确保Django服务运行在 http://127.0.0.1:8000")
        print("  3. 检查防火墙和网络连接")

if __name__ == "__main__":
    main()

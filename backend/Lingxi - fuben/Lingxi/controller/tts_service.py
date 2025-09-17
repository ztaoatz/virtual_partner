from django.shortcuts import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
import json
import requests
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def nahida_tts(request):
    """
    Nahida TTS服务API
    接收文本，返回Nahida语音音频流
    """
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        # 解析请求参数
        data = json.loads(request.body)
        text = data.get('text', '')
        
        if not text:
            return JsonResponse({'error': '文本内容不能为空'}, status=400)
        
        logger.info(f"TTS请求: {text[:50]}...")
        
        # 准备发送给TTS服务的参数
        payload = {
            "cha_name": "nahida",
            "text": text,
            "text_language": "多语种混合",
            "character_emotion": "default",
            "batch_size": 1,
            "stream": True
        }
        
        # 调用TTS服务
        tts_response = requests.post(
            "http://127.0.0.1:5000/tts", 
            json=payload, 
            stream=True,
            timeout=30
        )
        
        if tts_response.status_code == 200:
            # 创建HTTP响应，直接流式传输音频数据
            response = HttpResponse(
                tts_response.iter_content(chunk_size=1024),
                content_type='audio/wav'
            )
            response['Content-Disposition'] = 'inline; filename="nahida_tts.wav"'
            return response
        else:
            logger.error(f"TTS服务错误: {tts_response.status_code}")
            return JsonResponse({
                'error': 'TTS服务不可用',
                'status_code': tts_response.status_code
            }, status=503)
            
    except requests.exceptions.ConnectionError:
        logger.error("无法连接到TTS服务")
        return JsonResponse({
            'error': 'TTS服务连接失败，请确保TTS服务运行在 http://127.0.0.1:5000'
        }, status=503)
        
    except requests.exceptions.Timeout:
        logger.error("TTS服务超时")
        return JsonResponse({
            'error': 'TTS服务响应超时'
        }, status=504)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON格式'}, status=400)
        
    except Exception as e:
        logger.error(f"TTS服务异常: {str(e)}")
        return JsonResponse({
            'error': f'TTS服务异常: {str(e)}'
        }, status=500)

@csrf_exempt 
def check_tts_status(request):
    """
    检查TTS服务状态
    """
    try:
        # 发送测试请求到TTS服务，使用POST方法和minimal payload
        test_payload = {
            "cha_name": "nahida",
            "text": "test",
            "text_language": "多语种混合",
            "character_emotion": "default",
            "batch_size": 1,
            "stream": True
        }
        
        test_response = requests.post(
            "http://127.0.0.1:5000/tts", 
            json=test_payload,
            timeout=5,
            stream=True
        )
        
        if test_response.status_code == 200:
            # 只读取少量数据来验证响应
            test_response.close()
            return JsonResponse({
                'status': 'available',
                'message': 'TTS服务正常运行'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': f'TTS服务返回错误状态: {test_response.status_code}'
            })
            
    except requests.exceptions.ConnectionError:
        return JsonResponse({
            'status': 'unavailable',
            'message': 'TTS服务未启动或无法连接'
        })
        
    except requests.exceptions.Timeout:
        return JsonResponse({
            'status': 'timeout',
            'message': 'TTS服务响应超时'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'检查TTS服务时发生错误: {str(e)}'
        })

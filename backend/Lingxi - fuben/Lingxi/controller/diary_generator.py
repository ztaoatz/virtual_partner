from django.shortcuts import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from lingxiapp.models import ChatSession, ChatMessage, EmotionDiary
from users.models import UserProfile
import json
import uuid
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

def calculate_emotion_score(emotions_data):
    """
    计算情绪分值的函数
    基于情绪类型和强度进行加权计算
    """
    # 情绪权重映射
    emotion_weights = {
        '开心': 2.0,
        '快乐': 2.0,
        '兴奋': 1.8,
        '愉快': 1.5,
        '喜悦': 1.8,
        '满足': 1.2,
        '平静': 0.8,
        '安静': 0.5,
        '轻松': 1.0,
        '舒适': 1.0,
        '宁静': 0.8,
        '焦虑': -1.2,
        '紧张': -1.0,
        '担心': -1.0,
        '不安': -1.2,
        '忧虑': -1.0,
        '压力': -1.2,
        '难过': -1.5,
        '伤心': -1.8,
        '悲伤': -1.8,
        '沮丧': -1.5,
        '失落': -1.2,
        '郁闷': -1.0,
        '愤怒': -2.0,
        '生气': -1.8,
        '烦躁': -1.5,
        '恼火': -1.5,
        '气愤': -1.8,
        '疲惫': -0.5,
        '累': -0.5,
        '疲劳': -0.5,
        '困': -0.3,
        '乏力': -0.5
    }
    
    if not emotions_data:
        return 0.0
    
    total_score = 0.0
    total_intensity = 0
    
    for emotion_item in emotions_data:
        if isinstance(emotion_item, dict):
            emotion = emotion_item.get('emotion', '')
            intensity = emotion_item.get('intensity', 0)
        elif isinstance(emotion_item, str):
            emotion = emotion_item
            intensity = 50  # 默认强度
        else:
            continue
        
        weight = emotion_weights.get(emotion, 0.0)
        total_score += weight * intensity
        total_intensity += intensity
    
    # 归一化到0-100范围，50为中性
    if total_intensity > 0:
        normalized_score = 50 + (total_score / total_intensity) * 25
        return max(0, min(100, normalized_score))
    
    return 50.0  # 中性分值

@csrf_exempt
def generate_emotion_diary(request):
    """生成用户的情绪日记"""
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        params = json.loads(request.body)
        user_id = params.get('user_id')
        target_date = params.get('date', datetime.now().strftime('%Y-%m-%d'))
        force_regenerate = params.get('force_regenerate', False)  # 是否强制重新生成
        
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        
        # 检查是否已存在该日期的日记
        try:
            existing_diary = EmotionDiary.objects.get(
                user=user,
                date=target_date
            )
            if not force_regenerate:
                # 如果已存在且不强制重新生成，返回现有日记
                return JsonResponse({
                    'success': True,
                    'diary': {
                        'id': str(existing_diary.diary_id),
                        'content': existing_diary.content,
                        'emotions': json.loads(existing_diary.emotions) if existing_diary.emotions else [],
                        'main_topic': existing_diary.main_topic,
                        'message_count': existing_diary.message_count,
                        'date': existing_diary.date.strftime('%Y-%m-%d'),
                        'created_at': existing_diary.created_at.isoformat(),
                        'is_regenerated': False
                    }
                })
        except EmotionDiary.DoesNotExist:
            existing_diary = None
        
        # 获取指定日期的聊天记录
        target_datetime = datetime.strptime(target_date, '%Y-%m-%d').date()
        start_datetime = datetime.combine(target_datetime, datetime.min.time())
        end_datetime = datetime.combine(target_datetime, datetime.max.time())
        
        # 获取用户在指定日期的所有消息
        messages = ChatMessage.objects.filter(
            user=user,
            timestamp__gte=start_datetime,
            timestamp__lte=end_datetime
        ).order_by('timestamp')
        
        if not messages.exists():
            return JsonResponse({
                'error': f'{target_date} 没有聊天记录',
                'message': '该日期没有对话内容，无法生成情绪日记'
            }, status=400)
        
        # 准备聊天记录数据
        chat_history = []
        for msg in messages:
            chat_history.append({
                'text': msg.content,
                'isUser': msg.message_type == 'user',
                'timestamp': msg.timestamp.isoformat()
            })
        
        # 调用Ollama代理生成日记
        ollama_data = {
            'chat_history': chat_history,
            'user_name': profile.nickname or user.username,
            'date': target_date
        }
        print(f"调用Ollama生成日记，用户: {user.username}, 日期: {target_date}, 消息数: {len(chat_history)}")
        
        try:
            ollama_response = requests.post(
                'http://localhost:25674/generate-diary/',
                json=ollama_data,
                timeout=180  # 3分钟超时，与前端保持一致
            )
            
            if ollama_response.status_code != 200:
                print(f"Ollama代理返回错误: {ollama_response.status_code}, {ollama_response.text}")
                return JsonResponse({
                    'error': 'AI模型服务异常',
                    'details': f'状态码: {ollama_response.status_code}'
                }, status=500)
            
            diary_result = ollama_response.json()
            
            if not diary_result.get('success'):
                return JsonResponse({
                    'error': 'AI生成日记失败',
                    'details': diary_result.get('error', '未知错误')
                }, status=500)
            
        except requests.exceptions.RequestException as e:
            print(f"请求Ollama代理失败: {e}")
            return JsonResponse({
                'error': 'AI模型服务连接失败',
                'details': '请确认Ollama代理服务正在运行'
            }, status=500)
        
        # 计算情绪分值
        emotions_data = diary_result.get('emotions', [])
        emotion_score = calculate_emotion_score(emotions_data)
        
        # 保存或更新情绪日记
        diary_data = {
            'content': diary_result.get('diary_content', ''),
            'emotions': json.dumps(emotions_data, ensure_ascii=False),
            'main_topic': diary_result.get('main_topic', '日常交流'),
            'message_count': len(chat_history),
            'emotion_score': emotion_score,
            'date': target_datetime
        }
        
        if existing_diary and force_regenerate:
            # 更新现有日记
            for key, value in diary_data.items():
                setattr(existing_diary, key, value)
            existing_diary.updated_at = timezone.now()
            existing_diary.save()
            diary_obj = existing_diary
        else:
            # 创建新日记
            diary_obj = EmotionDiary.objects.create(
                user=user,
                **diary_data
            )
        
        return JsonResponse({
            'success': True,
            'diary': {
                'id': str(diary_obj.diary_id),
                'content': diary_obj.content,
                'emotions': json.loads(diary_obj.emotions) if diary_obj.emotions else [],
                'main_topic': diary_obj.main_topic,
                'message_count': diary_obj.message_count,
                'emotion_score': diary_obj.emotion_score,
                'date': diary_obj.date.strftime('%Y-%m-%d'),
                'created_at': diary_obj.created_at.isoformat(),
                'is_regenerated': force_regenerate and existing_diary is not None
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '请求数据格式错误'}, status=400)
    except Exception as e:
        print(f"生成情绪日记错误: {e}")
        return JsonResponse({'error': f'生成日记失败: {str(e)}'}, status=500)

@csrf_exempt
def get_emotion_diary(request):
    """获取用户指定日期的情绪日记"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    try:
        user_id = request.GET.get('user_id')
        target_date = request.GET.get('date', datetime.now().strftime('%Y-%m-%d'))
        
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        
        # 查找指定日期的日记
        try:
            diary = EmotionDiary.objects.get(
                user=user,
                date=target_date
            )
            return JsonResponse({
                'success': True,
                'diary': {
                    'id': str(diary.diary_id),
                    'content': diary.content,
                    'emotions': json.loads(diary.emotions) if diary.emotions else [],
                    'main_topic': diary.main_topic,
                    'message_count': diary.message_count,
                    'emotion_score': diary.emotion_score,
                    'date': diary.date.strftime('%Y-%m-%d'),
                    'created_at': diary.created_at.isoformat()
                }
            })
            
        except EmotionDiary.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': '该日期没有情绪日记'
            })
            
    except Exception as e:
        print(f"获取情绪日记错误: {e}")
        return JsonResponse({'error': f'获取日记失败: {str(e)}'}, status=500)

@csrf_exempt
def get_diary_dates(request):
    """获取用户有日记的所有日期"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    try:
        user_id = request.GET.get('user_id')
        
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        
        # 获取用户所有的日记日期
        diary_dates = EmotionDiary.objects.filter(
            user=user
        ).values_list('date', flat=True).order_by('-date')
        
        dates_list = [date.strftime('%Y-%m-%d') for date in diary_dates]
        
        return JsonResponse({
            'success': True,
            'dates': dates_list
        })
        
    except Exception as e:
        print(f"获取日记日期错误: {e}")
        return JsonResponse({'error': f'获取日记日期失败: {str(e)}'}, status=500)

@csrf_exempt
def get_emotion_trend(request):
    """获取用户最近10天的情绪趋势数据"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    try:
        user_id = request.GET.get('user_id')
        days = int(request.GET.get('days', 10))  # 默认获取最近10天
        
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            # 更友好的错误处理：区分未登录用户和不存在的用户
            return JsonResponse({
                'error': '用户认证失败', 
                'message': '请先登录后再查看趋势图',
                'code': 'USER_NOT_AUTHENTICATED'
            }, status=401)
        
        # 获取用户最近指定天数的日记，按日期排序
        diaries = EmotionDiary.objects.filter(
            user=user
        ).order_by('-date')[:days]
          # 构建趋势数据
        trend_data = []
        for diary in reversed(diaries):  # 反转以获得时间正序
            trend_data.append({
                'date': diary.date.strftime('%Y-%m-%d'),
                'emotion_score': diary.emotion_score,
                'main_emotion': diary.main_topic or '日常',
                'message_count': diary.message_count,
                'emotions': json.loads(diary.emotions) if diary.emotions else []
            })
        
        # 如果没有日记数据，返回友好提示
        if not trend_data:
            return JsonResponse({
                'success': True,
                'trend_data': [],
                'total_days': 0,
                'message': '暂无情绪日记数据，请先生成一些日记后再查看趋势图'
            })
        
        return JsonResponse({
            'success': True,
            'trend_data': trend_data,
            'total_days': len(trend_data)
        })
        
    except Exception as e:
        print(f"获取情绪趋势错误: {e}")
        return JsonResponse({'error': f'获取情绪趋势失败: {str(e)}'}, status=500)

@csrf_exempt
def delete_emotion_diary(request):
    """删除用户指定日期的情绪日记"""
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST请求'}, status=405)
    
    try:
        params = json.loads(request.body)
        user_id = params.get('user_id')
        target_date = params.get('date')
        
        if not user_id or not target_date:
            return JsonResponse({'error': '缺少必要参数'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        
        # 删除指定日期的日记
        try:
            diary = EmotionDiary.objects.get(
                user=user,
                date=target_date
            )
            diary.delete()
            
            return JsonResponse({
                'success': True,
                'message': '日记删除成功'
            })
            
        except EmotionDiary.DoesNotExist:
            return JsonResponse({
                'error': '该日期没有情绪日记'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': '请求数据格式错误'}, status=400)
    except Exception as e:
        print(f"删除情绪日记错误: {e}")
        return JsonResponse({'error': f'删除日记失败: {str(e)}'}, status=500)
        
        if not messages.exists():
            return JsonResponse({'error': '该日期没有聊天记录'}, status=404)
        
        # 转换消息格式
        chat_history = []
        for msg in reversed(messages):  # 反转以获得时间顺序
            chat_history.append({
                'text': msg.content,
                'isUser': msg.message_type == 'user',
                'timestamp': msg.timestamp.isoformat(),
                'emotion': msg.emotion
            })
        
        # 准备发送给Ollama代理的数据
        diary_request = {
            'chat_history': chat_history,
            'user_name': profile.nickname or user.username,
            'date': target_date.strftime('%Y年%m月%d日')
        }
        
        print(f"发送日记生成请求: 用户={profile.nickname}, 消息数={len(chat_history)}")
        
        # 调用Ollama代理生成日记
        response = requests.post(
            'http://localhost:25674/generate-diary/',
            json=diary_request,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            
            if result.get('success'):
                return JsonResponse({
                    'success': True,
                    'diary': {
                        'content': result.get('diary_content', ''),
                        'emotions': result.get('emotions', []),
                        'main_topic': result.get('main_topic', ''),
                        'message_count': result.get('message_count', 0),
                        'date': target_date.strftime('%Y-%m-%d'),
                        'user_name': profile.nickname or user.username
                    }
                })
            else:
                return JsonResponse({'error': result.get('error', '生成失败')}, status=500)
        else:
            return JsonResponse({'error': 'AI服务暂时不可用'}, status=503)
            
    except requests.exceptions.Timeout:
        return JsonResponse({'error': '请求超时，请稍后重试'}, status=504)
    except requests.exceptions.ConnectionError:
        return JsonResponse({'error': 'AI服务连接失败'}, status=503)
    except Exception as e:
        print(f"生成情绪日记错误: {e}")
        return JsonResponse({'error': '服务器内部错误'}, status=500)

@csrf_exempt
def get_diary_history(request):
    """获取用户的日记历史"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    try:
        user_id = request.GET.get('user_id')
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        
        # 获取用户有聊天记录的日期
        chat_dates = ChatMessage.objects.filter(user=user)\
            .extra({'date': "date(timestamp)"})\
            .values('date')\
            .distinct()\
            .order_by('-date')[:30]  # 最近30天
        
        diary_dates = []
        for item in chat_dates:
            date_obj = item['date']
            # 检查该日期是否有足够的消息来生成日记
            message_count = ChatMessage.objects.filter(
                user=user,
                timestamp__date=date_obj
            ).count()
            
            if message_count >= 2:  # 至少需要2条消息（1个对话回合）
                diary_dates.append({
                    'date': date_obj.strftime('%Y-%m-%d'),
                    'message_count': message_count,
                    'formatted_date': date_obj.strftime('%m月%d日')
                })
        
        return JsonResponse({
            'success': True,
            'diary_dates': diary_dates,
            'user_name': profile.nickname or user.username
        })
        
    except Exception as e:
        print(f"获取日记历史错误: {e}")
        return JsonResponse({'error': '服务器内部错误'}, status=500)

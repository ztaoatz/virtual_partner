@csrf_exempt
def check_emotion_intervention(request):
    """检查用户是否需要情绪干预"""
    if request.method != 'GET':
        return JsonResponse({'error': '只支持GET请求'}, status=405)
    
    try:
        user_id = request.GET.get('user_id')
        days = int(request.GET.get('days', 7))  # 默认检查最近7天
        
        if not user_id:
            return JsonResponse({'error': '缺少用户ID'}, status=400)
        
        # 获取用户信息
        try:
            profile = UserProfile.objects.get(external_user_id=user_id)
            user = profile.user
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': '用户不存在'}, status=404)
        
        # 获取用户最近的情绪日记（按日期正序）
        all_diaries = EmotionDiary.objects.filter(user=user).order_by('date')
        recent_diaries = list(all_diaries)[-days:] if len(all_diaries) > days else list(all_diaries)
        
        if not recent_diaries:
            return JsonResponse({
                'success': True,
                'intervention_needed': False,
                'message': '用户暂无情绪日记数据'
            })
        
        # 获取历史分值和当前分值
        all_scores = [diary.emotion_score for diary in recent_diaries]
        current_score = all_scores[-1]  # 最新分值
        recent_scores = all_scores[:-1] if len(all_scores) > 1 else []  # 历史分值
        
        print(f"调试信息 - 用户{user.username}:")
        print(f"  所有分值: {all_scores}")
        print(f"  当前分值: {current_score}")
        print(f"  历史分值: {recent_scores}")
        
        # 检查是否需要干预
        intervention_check = check_emotional_crisis_intervention(user, recent_scores, current_score)
        
        if intervention_check:
            intervention_data = generate_intervention_suggestions(intervention_check)
            return JsonResponse({
                'success': True,
                'intervention_needed': True,
                'intervention': intervention_data,
                'user_stats': {
                    'current_score': current_score,
                    'avg_score': intervention_check['avg_score'],
                    'continuous_days': intervention_check['continuous_days'],
                    'crisis_days': intervention_check['crisis_days']
                }
            })
        else:
            return JsonResponse({
                'success': True,
                'intervention_needed': False,
                'user_stats': {
                    'current_score': current_score,
                    'avg_score': sum(all_scores) / len(all_scores),
                    'total_days': len(recent_diaries)
                },
                'message': '用户情绪状态正常'
            })
    
    except Exception as e:
        print(f"检查情绪干预错误: {e}")
        return JsonResponse({'error': f'检查失败: {str(e)}'}, status=500)

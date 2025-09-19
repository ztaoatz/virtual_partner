from flask import Flask, request, jsonify
import requests
import json
import time
import re

app = Flask(__name__)

# Ollama默认运行在11434端口
OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route('/chat/', methods=['POST'])
def chat():
    try:
        # 接收Django发送的数据
        data = request.json
        print(f"接收到请求: {data}")
        
        # 构建发送给Ollama的提示词
        system_prompt = data.get('system', '')
        user_text = data.get('text', '')
        
        # 组合系统提示和用户输入
        full_prompt = f"System: {system_prompt}\n\nUser: {user_text}\n\nAssistant:"
        
        # 发送请求给Ollama
        ollama_request = {
            "model": "qwen",  # 聊天功能使用qwen2.5:3b模型
            "prompt": full_prompt,
            "stream": False,  # 不使用流式输出
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 1000
            }
        }
        
        print(f"发送给Ollama: {ollama_request}")
        
        # 调用Ollama API
        response = requests.post(
            OLLAMA_URL, 
            json=ollama_request,
            timeout=60  # 设置超时时间
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # 返回与原项目兼容的格式
            return jsonify({
                "result": result.get('response', ''),
                "history": []
            })
        else:
            print(f"Ollama返回错误: {response.status_code}, {response.text}")
            return jsonify({"error": "Ollama服务错误"}), 500
            
    except Exception as e:
        print(f"代理服务错误: {str(e)}")
        return jsonify({"error": f"代理服务错误: {str(e)}"}), 500

@app.route('/generate-diary/', methods=['POST'])
def generate_diary():
    """生成情绪日记 - 优化版本"""
    try:
        # 接收聊天记录数据
        data = request.json
        print(f"接收到日记生成请求: {data}")
        
        chat_history = data.get('chat_history', [])
        user_name = data.get('user_name', '用户')
        date = data.get('date', '')
        
        if not chat_history:
            return jsonify({"error": "没有聊天记录"}), 400
        
        # 构建聊天记录摘要
        conversations = []
        for msg in chat_history:
            role = "用户" if msg.get('isUser') else "AI助手"
            content = msg.get('text', '')
            conversations.append(f"{role}: {content}")
        
        chat_summary = "\n".join(conversations)
        
        # 构建专门用于情绪日记的提示词 - 优化版本
        diary_prompt = f"""作为专业心理健康助手，请为用户生成情绪日记。

用户: {user_name}
日期: {date}

对话记录:
{chat_summary}

请生成一份简洁的情绪日记，包含：
1. 今日情绪状态和变化
2. 主要交流话题
3. 积极感受和收获
4. 需要关注的方面
5. 温暖的鼓励和建议

要求：
- 语调温暖理解
- 字数200-280字
- 结构清晰
- 内容积极正面

情绪日记:"""
          # 发送请求给Ollama - 优化版本，关闭思考功能
        ollama_request = {
            "model": "qwen3:4b",
            "prompt": diary_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,  # 降低温度提高稳定性
                "top_p": 0.8,        # 减少随机性
                "max_tokens": 600,   # 增加最大token数
                "repeat_penalty": 1.1,  # 避免重复内容
                "thinking": False    # 关闭思考功能，避免生成<think>标签
            }
        }
        print(f"发送给Ollama生成日记: {ollama_request}")
        
        # 添加重试机制
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                print(f"尝试生成日记 (第 {retry_count + 1} 次)")
                  # 调用Ollama API，延长超时时间
                response = requests.post(
                    OLLAMA_URL, 
                    json=ollama_request,
                    timeout=300  # 延长到5分钟超时，避免因思考时间长导致超时
                )
                
                if response.status_code == 200:
                    result = response.json()
                    raw_diary_content = result.get('response', '')
                    
                    # 检查生成内容是否有效
                    if raw_diary_content and len(raw_diary_content.strip()) > 50:
                        # 清理AI思考过程标签
                        diary_content = clean_thinking_tags(raw_diary_content)
                        
                        # 验证清理后的内容长度
                        if len(diary_content.strip()) < 30:
                            print(f"清理后内容过短，重试 ({retry_count + 1}/{max_retries + 1})")
                            retry_count += 1
                            continue
                        
                        # 简单的情绪分析
                        emotions = analyze_emotions(chat_summary)
                        main_topic = extract_main_topic(chat_summary)
                        
                        print(f"日记生成成功，长度: {len(diary_content)} 字符")
                        return jsonify({
                            "success": True,
                            "diary_content": diary_content,
                            "emotions": emotions,
                            "main_topic": main_topic,
                            "message_count": len(chat_history)
                        })
                    else:
                        print(f"生成内容过短或为空，尝试重试 ({retry_count + 1}/{max_retries + 1})")
                        retry_count += 1
                        if retry_count <= max_retries:
                            time.sleep(1)  # 短暂等待后重试
                        continue
                else:
                    print(f"Ollama返回错误: {response.status_code}, {response.text}")
                    if retry_count < max_retries:
                        retry_count += 1
                        print(f"HTTP错误，重试第 {retry_count} 次")
                        time.sleep(2)
                        continue
                    else:
                        return jsonify({"error": "AI模型服务异常"}), 500
                        
            except requests.exceptions.Timeout:
                retry_count += 1
                if retry_count <= max_retries:
                    print(f"请求超时，重试第 {retry_count} 次")
                    time.sleep(2)
                    continue
                else:
                    return jsonify({"error": "请求超时，AI模型响应时间过长"}), 500
            except Exception as e:
                print(f"请求异常: {str(e)}")
                retry_count += 1
                if retry_count <= max_retries:
                    time.sleep(2)
                    continue
                else:
                    return jsonify({"error": f"日记生成异常: {str(e)}"}), 500
        
        # 所有重试都失败
        return jsonify({"error": "日记生成失败，请稍后重试"}), 500
            
    except Exception as e:
        print(f"日记生成错误: {str(e)}")
        return jsonify({"error": f"日记生成错误: {str(e)}"}), 500

def analyze_emotions(text):
    """简单的情绪分析"""
    emotion_keywords = {
        '开心': ['开心', '高兴', '快乐', '兴奋', '愉快', '喜悦', '满意', '欣慰'],
        '难过': ['难过', '伤心', '悲伤', '沮丧', '失落', '郁闷', '痛苦', '忧伤'],
        '焦虑': ['焦虑', '紧张', '担心', '不安', '忧虑', '压力', '紧迫', '恐慌'],
        '愤怒': ['愤怒', '生气', '烦躁', '恼火', '气愤', '愤慨', '恼怒'],
        '平静': ['平静', '安静', '轻松', '舒适', '宁静', '淡定', '从容'],
        '疲惫': ['累', '疲惫', '疲劳', '困', '乏力', '疲倦', '劳累'],
        '兴奋': ['兴奋', '激动', '期待', '热情', '振奋', '活力'],
        '困惑': ['困惑', '迷茫', '不解', '疑惑', '不清楚', '摸不着头脑']
    }
    
    detected_emotions = []
    text_lower = text.lower()
    
    for emotion, keywords in emotion_keywords.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        if score > 0:
            detected_emotions.append({
                'emotion': emotion,
                'intensity': min(score * 20, 100)  # 简单的强度评分
            })
    
    # 按强度排序，返回前3个主要情绪
    detected_emotions.sort(key=lambda x: x['intensity'], reverse=True)
    return detected_emotions[:3] if detected_emotions else [{'emotion': '平静', 'intensity': 50}]

def extract_main_topic(text):
    """提取主要话题"""
    topics = [
        {'name': '工作学习', 'keywords': ['工作', '学习', '项目', '任务', '考试', '作业', '职场', '同事', '老板', '学校']},
        {'name': '人际关系', 'keywords': ['朋友', '家人', '同事', '关系', '交流', '沟通', '聊天', '社交', '朋友圈']},
        {'name': '健康生活', 'keywords': ['健康', '运动', '饮食', '睡眠', '休息', '锻炼', '身体', '医院', '药物']},
        {'name': '情感表达', 'keywords': ['感受', '情绪', '心情', '想法', '感觉', '体验', '内心', '情感']},
        {'name': '兴趣爱好', 'keywords': ['游戏', '电影', '音乐', '阅读', '旅行', '美食', '艺术', '摄影', '运动']},
        {'name': '生活日常', 'keywords': ['日常', '生活', '今天', '昨天', '计划', '安排', '家务', '购物']},
        {'name': '技术问题', 'keywords': ['技术', '编程', '代码', '软件', '电脑', '手机', '网络', 'bug']},
        {'name': '未来规划', 'keywords': ['计划', '目标', '未来', '规划', '梦想', '期望', '打算', '想要']}
    ]
    
    text_lower = text.lower()
    topic_scores = []
    
    for topic in topics:
        score = sum(1 for keyword in topic['keywords'] if keyword in text_lower)
        if score > 0:
            topic_scores.append({'name': topic['name'], 'score': score})
    
    if topic_scores:
        topic_scores.sort(key=lambda x: x['score'], reverse=True)
        return topic_scores[0]['name']
    else:
        return '日常交流'

def clean_thinking_tags(text):
    """清理AI生成内容中的思考过程标签 - 增强版本"""
    # 移除 <think>...</think> 标签及其内容
    # 使用非贪婪匹配，支持多行内容
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # 移除可能的单独的 <think> 或 </think> 标签
    cleaned_text = re.sub(r'</?think>', '', cleaned_text, flags=re.IGNORECASE)
    
    # 移除其他常见的AI思考标签
    cleaned_text = re.sub(r'<thinking>.*?</thinking>', '', cleaned_text, flags=re.DOTALL | re.IGNORECASE)
    cleaned_text = re.sub(r'</?thinking>', '', cleaned_text, flags=re.IGNORECASE)
    
    # 清理多余的空行和首尾空白
    cleaned_text = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned_text)  # 多个空行合并为两个
    cleaned_text = cleaned_text.strip()
    
    return cleaned_text

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口 - 增强版本"""
    try:
        # 测试Ollama连接
        test_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if test_response.status_code == 200:
            models = test_response.json().get('models', [])
            available_models = [model.get('name', '') for model in models]
            return jsonify({
                "status": "healthy", 
                "ollama": "connected",
                "available_models": available_models,
                "timestamp": time.time()
            })
        else:
            return jsonify({
                "status": "unhealthy", 
                "ollama": "disconnected",
                "error": f"HTTP {test_response.status_code}"
            }), 500
    except Exception as e:
        return jsonify({
            "status": "unhealthy", 
            "ollama": "disconnected",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 启动Ollama代理服务 (优化版本)...")
    print("📍 监听地址: http://localhost:25674")
    print("🔗 Ollama地址: http://localhost:11434")
    print("💡 健康检查: http://localhost:25674/health")
    print("🔄 重试机制: 最多3次尝试")
    print("⏱️  超时设置: 聊天60s，日记120s")
    
    app.run(host='localhost', port=25674, debug=True)

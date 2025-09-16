from flask import Flask, request, jsonify
import requests
import json

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
        full_prompt = f"System: {system_prompt}\n\nUser: {user_text}\n\nAssistant:"        # 发送请求给Ollama
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
    """生成情绪日记"""
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
        
        # 构建专门用于情绪日记的提示词
        diary_prompt = f"""你是一个专业的心理健康助手，请根据以下对话记录为用户生成一份情绪日记。

用户姓名: {user_name}
日期: {date}

对话记录:
{chat_summary}

请分析这些对话并生成一份结构化的情绪日记，包含以下内容：
1. 主要情绪状态（开心、难过、焦虑、平静等）
2. 今日主要话题和关注点
3. 情绪变化分析
4. 积极方面的总结
5. 需要关注或改善的方面
6. 鼓励性的结语

请用温暖、理解的语调写作，字数控制在200-300字。

情绪日记:"""
        
        # 发送请求给Ollama
        ollama_request = {
            "model": "qwen3:4b",
            "prompt": diary_prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,  # 稍高的创造性
                "top_p": 0.9,
                "max_tokens": 800
            }
        }
        
        print(f"发送给Ollama生成日记: {ollama_request}")
        
        # 调用Ollama API
        response = requests.post(
            OLLAMA_URL, 
            json=ollama_request,
            timeout=90  # 日记生成可能需要更长时间
        )
        
        if response.status_code == 200:
            result = response.json()
            diary_content = result.get('response', '')
            
            # 简单的情绪分析
            emotions = analyze_emotions(chat_summary)
            main_topic = extract_main_topic(chat_summary)
            
            return jsonify({
                "success": True,
                "diary_content": diary_content,
                "emotions": emotions,
                "main_topic": main_topic,
                "message_count": len(chat_history)
            })
        else:
            print(f"Ollama返回错误: {response.status_code}, {response.text}")
            return jsonify({"error": "日记生成失败"}), 500
            
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

@app.route('/health', methods=['GET'])
def health():
    """健康检查接口"""
    try:
        # 测试Ollama连接
        test_response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if test_response.status_code == 200:
            return jsonify({"status": "healthy", "ollama": "connected"})
        else:
            return jsonify({"status": "unhealthy", "ollama": "disconnected"}), 500
    except:
        return jsonify({"status": "unhealthy", "ollama": "disconnected"}), 500

if __name__ == '__main__':
    print("🚀 启动Ollama代理服务...")
    print("📍 监听地址: http://localhost:25674")
    print("🔗 Ollama地址: http://localhost:11434")
    print("💡 健康检查: http://localhost:25674/health")
    
    app.run(host='localhost', port=25674, debug=True)
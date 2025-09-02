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
        full_prompt = f"System: {system_prompt}\n\nUser: {user_text}\n\nAssistant:"
        
        # 发送请求给Ollama
        ollama_request = {
            "model": "qwen",  # 你运行的模型名称
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
# 数据流程实际示例

## 用户操作：
1. 打开浏览器访问前端页面
2. 选择场景："向长辈敬酒"
3. 在文本框输入："帮我生成一个敬酒词"
4. 点击"发送"按钮

## 前端处理：
```javascript
// 用户输入存储在 userInput 变量中
userInput: "帮我生成一个敬酒词"

// 点击发送时执行的代码
submit() {
  axios.post('http://127.0.0.1:8000/chat/', {
    "prompt": this.userInput,  // "帮我生成一个敬酒词"
    "history": '',
    "system": '你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。'
  })
}
```

## HTTP请求：
```http
POST /chat/ HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
  "prompt": "帮我生成一个敬酒词",
  "history": "",
  "system": "你现在是由SocialAI开发的人情世故大模型，你的任务是洞察人情世故、提供合适的交往策略和建议。"
}
```

## 后端处理：
```python
def getchat(request):
    # 接收到的 request.body 内容：
    # '{"prompt":"帮我生成一个敬酒词","history":"","system":"你现在是由SocialAI开发的人情世故大模型..."}'
    
    params = json.loads(request.body)
    # params = {
    #     "prompt": "帮我生成一个敬酒词",
    #     "history": "",
    #     "system": "你现在是由SocialAI开发的人情世故大模型..."
    # }
    
    data = {
        "text": params['prompt'],      # "帮我生成一个敬酒词"
        "system": params['system'],   # "你现在是由SocialAI开发的人情世故大模型..."
        "history": []
    }
    
    # 转发给AI模型
    res = requests.post('http://localhost:25674/chat/', data=json.dumps(data))
```

## AI模型返回：
```json
{
  "result": "尊敬的长辈们，感谢您们多年来的关爱和指导。今天举杯，愿您们身体健康，家庭幸福。这杯酒，敬您们！",
  "history": [...]
}
```

## 前端接收并显示：
```javascript
.then(result => {
  this.responseText = result.data.result;
  // responseText 现在包含 AI 生成的敬酒词
});
```

## 用户看到的结果：
在前端页面的文本框中显示：
"尊敬的长辈们，感谢您们多年来的关爱和指导。今天举杯，愿您们身体健康，家庭幸福。这杯酒，敬您们！"

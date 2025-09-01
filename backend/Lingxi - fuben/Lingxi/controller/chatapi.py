from ..system.tools import jsonutil
from django.shortcuts import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import JsonResponse

@csrf_exempt
def getchat(request):
    print("开始获取对话")                                #在终端中输出开始对话，表示函数开始运行
    headers = {'Content-Type': 'application/json'}    #http请求头部
    params = json.loads(request.body)                 #读取request请求中的数据包
    print(params)                                     #在终端中输出请求，表示数据接受正常
    history = []
    data = {                                          #创建向服务器发送的数据包，包含三个变量"text"、"system"和"history"
        "text": params['prompt'],
        "system": params['system'],
        "history": history
    }
    print(data)                                       #在终端中打印数据包，表示程序正常运行
    res = requests.post(                              #向服务器发送请求，并将返回的数据存储在"res"变量中
                 url='http://localhost:25674/chat/',
                 headers=headers,
                 data=json.dumps(data))
    print("完成生成")                                   #在终端中输出完成生成，表示模型成功生成回复并发送成功，程序运行正常
    d = res.json()                                    #将返回文件打包为 json
    return JsonResponse(d)                            #返回请求

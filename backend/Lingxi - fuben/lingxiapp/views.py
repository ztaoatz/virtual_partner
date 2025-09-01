from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.viewsets import ModelViewSet
from lingxiapp.models import UserInfo
from lingxiapp.serializer import UserInfoSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from lingxiapp.filter import UserInfoFilter  # 导入筛选器
import json

from django.shortcuts import render
# import HttpResponse from django.urls
from django.http import HttpResponse


# this is the home view for handling home page logic
def home(request):
    return HttpResponse('The Home Page')


# this is the view for handling errors
def error_handler(request):
    return HttpResponse('404 Page')

@api_view(['POST'])
def generate_response(request):
    data = request.data
    prompt = data.get('prompt')
    history = []
    # 调用大模型进行生成内容
    response, history = call_model_to_generate_response(prompt, history)
    return Response({'response': response}, status=status.HTTP_200_OK)


def call_model_to_generate_response(prompt, history=None):
    # 这里需要实现与大模型的交互
    # 使用假设的大模型 API 地址
    url = 'http://localhost:6006/chat/'
    headers = {'Content-Type': 'application/json'}
    data = {
        "text": prompt,
        "history": history
    }
    try:
        # 发送 POST 请求到大模型的 API
        response = requests.post(
            url,
            headers=headers,
            data=json.dumps(data),
            verify=False
        )
        d = response.json()
        result, history = d['result'], d['history']
        # 检查请求是否成功
        response.raise_for_status()
        return result, history
    except requests.RequestException as e:
        # 处理请求异常
        return f'Error: {str(e)}'


class UserInfoViewSet(ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserInfoSerializer
    filter_class = UserInfoFilter  # 添加筛选器
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['username']


def index(request):
    return HttpResponse("Welcome to the API!")

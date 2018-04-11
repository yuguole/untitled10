from django.shortcuts import render
#coding=utf-8
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse,FileResponse
from Iknow.models import UserInfo
from Iknow.Serializers import UserSerializer
from rest_framework.renderers import JSONRenderer
from django.core import serializers
from django.db.models import Q
from django.core.files import File
import json,os
import ast
from rest_framework.decorators import api_view
# from django.core.servers.basehttp import FileWrapper
from wsgiref.util import FileWrapper
# from django.forms.models import model_to_dict
# 路由的处理方法在这里。
def index(request):
    return HttpResponse('Test..user')
@api_view(['POST'])
def login(request):
    # 考虑到出错的可能性，一开始就设置为
    context = {'status': 400, 'content': 'null'}
    if request.method == "POST":
        username = request.data.get('username', )
        password = request.data.get('password')
        try:
            user = UserInfo.maneger.get(username=username, password=password)
            context['status'] = 200
        except:
            context['status'] == 400
        if context['status'] == 200:
            serializer = UserSerializer(user)
            context['content'] = serializer.data
        else:
            context['content'] = "null"
        content = JSONRenderer().render(context)
        return HttpResponse(content)
    return HttpResponse(JSONRenderer().render(context))


# 用户注册的事件处理
# 用户注册和登录
# 用户名字或者QQ号码被绑定的话返回500.这里采用了Q对象
# 测试成功
@api_view(['POST'])
def register(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            testuser = UserInfo.maneger.filter(username=username)
            if testuser:
                context['status'] = 500
            else:
                user = UserInfo.maneger.create(username, password)
                user.save()
                context['status'] = 200
        except Exception:
            context['status'] = 400
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


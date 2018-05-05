from django.shortcuts import render
#coding=utf-8
from django.http import HttpResponse,JsonResponse,StreamingHttpResponse,FileResponse
from Iknow.models import*
from Iknow.Serializers import*
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
            if user:
                context['status'] = 200
        except:
            context['status'] = 400
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
            context['status'] = 600
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

@api_view(['POST'])
def addlabel(request):
    context={'status':400,}
    if request.method == "POST":
        #获取到对象，之后序列化
        lb_title = request.data.get('lb_title')
        user = LabelInfo.maneger.filter(lb_title=lb_title)
        if user:
            context['status'] = 500
        else:
            lb=LabelInfo(lb_title=lb_title)
            lb.save()
            if lb:
                context['status'] = 200
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


@api_view(['POST'])
def addask(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        askuser = request.data.get('askuser')
        asktitle = request.data.get('asktitle')
        askdetail = request.data.get('askdetail')
        asklabel=request.POST.getlist('asklabel[]')
        try:
            user1=UserInfo.maneger.get(username=askuser)#现在User表中查询出前端选中的用户对应对象
            testask=AskInfo.maneger.filter(ask_title=asktitle)
            if testask:
                context['status'] = 500#有相同的问题
            else:
                a1=AskInfo(ask_title=asktitle,ask_details=askdetail,ask_user=user1)
                a1.save()#普通数据和外键插入的数据先save
                context['status'] = 200#除标签外保存
        #a1=AskInfo.objects.get(ask_title=asktitle)#查出书名对象，也就是获取要插入的多对多数据项
                a2 = AskInfo.maneger.get(ask_title=asktitle)
                if len(asklabel)==1:
                    l1=LabelInfo.maneger.get(lb_title=asklabel[0])#在标签表中查询出前端选中的标签对象
                    a2.ask_label.add(l1)
                    a2.save()
                    if a2:
                        context['status'] = 200#全保存
                    else:
                        context['status'] = 300#标签未保存
            #a1.ask_label.add(asklabel[0])#多对多使用add方法进行插入
            #a1.save()
                elif len(asklabel)==0:#当前没有选中标签
                    context['status']=510#没有选中标签
                else:#如果有很多标签，循环插入标签
                    for lb in asklabel:
                        l2 = LabelInfo.maneger.get(lb_title=lb)  #
                        a2.ask_label.add(l2)#使用add加入
                    a2.save()
                    if a2:
                        context['status'] = 200
                    else:
                        context['status'] = 310
        except:
            context['status'] = 0
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


@api_view(['POST'])
def addreply(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        reaskid = request.data.get('reaskid')
        redetail = request.data.get('redetail')
        reuser = request.data.get('reuser')
        user1 = UserInfo.maneger.get(username=reuser)  # 现在User表中查询出前端选中的用户对应对象
        #ask1=AskInfo.maneger.get(id=reaskid)#找出对应id的问题表对象
        ask1=AskInfo.maneger.get(id=reaskid)#在问题表中查询出前端选中的用户对象
        r1 = ReplyInfo(re_details=redetail,re_ask=ask1,re_user=user1)
        r1.save()  # 普通数据和外键插入的数据先save
        if r1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500

        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

@api_view(['POST'])
def showask(request):
    context = {'status': 400,'content':'null'}
    if request.method == "POST":
        # 获取到对象，之后序列化
        ask_list=AskInfo.maneger.all().values_list('ask_title','ask_details','ask_user__username','ask_time',)#'ask_details','ask_user','ask_time')
        ask_list1=convert_to_json_string_2(ask_list)

        return HttpResponse(ask_list1)
    #return HttpResponse(JSONRenderer().render(context))
        #return render(request,{'asklist':ask_list})
    return HttpResponse(JSONRenderer().render(context))

def convert_to_json_string_2(data):
    #label11=[]
    #for i in data:
        #ask11=AskInfo.maneger.get(ask_title=i[0])
        #label11=ask11.ask_label.get("askinfo__ask_label")
        return json.dumps({'ask':
                           [{'title': i[0],
                             'details': i[1],
                             'askuser':i[2],
                             'asktime':str(i[3]),
                            # 'asklable':[{j[0]}for j in label11],
                             } for i in data]}, indent=4)

@api_view(['POST'])
def showlabel(request):
    context = {'status': 400,'content':'null'}
    if request.method == "POST":
        # 获取到对象，之后序列化
        label_list=LabelInfo.maneger.all().values_list('id','lb_title',)#'ask_details','ask_user','ask_time')
        label_list1=convert_to_json_string_label(label_list)

        return HttpResponse(label_list1)
    #return HttpResponse(JSONRenderer().render(context))
        #return render(request,{'asklist':ask_list})
    return HttpResponse(JSONRenderer().render(context))

def convert_to_json_string_label(data):
    #label11=[]
    #for i in data:
        #ask11=AskInfo.maneger.get(ask_title=i[0])
        #label11=ask11.ask_label.get("askinfo__ask_label")
        return json.dumps({'label':
                           [{'labelid': i[0],
                             'labeltitle': i[1],
                             } for i in data]}, indent=4)

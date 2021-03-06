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


#登录
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

#注册
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

#添加新的标签
@api_view(['POST'])
def addlabel(request):
    context={'status':400,}
    if request.method == "POST":
        #获取到对象，之后序列化
        lb_title = request.data.get('lb_title')
        label = LabelInfo.maneger.filter(lb_title=lb_title)
        if label:
            context['status'] = 500
        else:
            lb=LabelInfo(lb_title=lb_title)
            lb.save()
            if lb:
                context['status'] = 200
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#添加新的问题
@api_view(['POST'])
def addask(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        askuser = request.data.get('askuser')
        asktitle = request.data.get('asktitle')
        askdetail = request.data.get('askdetail')
        asktime=request.data.get('asktime')
        asklabel=request.data.getlist('asklabel',[])
        try:
            user1=UserInfo.maneger.get(username=askuser)#现在User表中查询出前端选中的用户对应对象
            testask=AskInfo.maneger.filter(ask_title=asktitle)
            if testask:
                context['status'] = 500#有相同的问题
            else:
                a1=AskInfo(ask_title=asktitle,ask_details=askdetail,ask_user=user1,ask_time=asktime)
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

#仅仅添加问题
@api_view(['POST'])
def add_ask(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        # 获取到对象，之后序列化
        askuser = request.data.get('askuser')
        asktitle = request.data.get('asktitle')
        askdetail = request.data.get('askdetail')
        asktime = request.data.get('asktime')
        try:
            user1=UserInfo.maneger.get(username=askuser)#现在User表中查询出前端选中的用户对应对象
            testask=AskInfo.maneger.filter(ask_title=asktitle)
            if testask:
                context['status'] = 500#有相同的问题
            else:
                a1=AskInfo(ask_title=asktitle,ask_details=askdetail,ask_user=user1,ask_time=asktime)
                a1.save()#普通数据和外键插入的数据先save
                if a1:
                    context['status'] = 200#除标签外保存
                else:
                    context['status']=600
        except:
            context['status'] = 0

        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#添加问题的标签
@api_view(['POST'])
def add_asklabel(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        asktitle = request.data.get('asktitle')
        asklabel=request.data.get('asklabel')
        try:
            a2 = AskInfo.maneger.get(ask_title=asktitle)
            l1=LabelInfo.maneger.get(lb_title=asklabel)#在标签表中查询出前端选中的标签对象
            a2.ask_label.add(l1)
            a2.save()
            if a2:
                context['status'] = 200#全保存
            else:
                context['status'] = 300#标签未保存
        except:
            context['status'] = 500
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


#添加回答问题
@api_view(['POST'])
def addreply(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        reaskid = request.data.get('reaskid')
        redetail = request.data.get('redetail')
        reuser = request.data.get('reuser')
        retime=request.data.get('retime')
        user1 = UserInfo.maneger.get(username=reuser)  # 现在User表中查询出前端选中的用户对应对象
        #ask1=AskInfo.maneger.get(id=reaskid)#找出对应id的问题表对象
        ask1=AskInfo.maneger.get(id=reaskid)#在问题表中查询出前端选中的用户对象
        r1 = ReplyInfo(re_details=redetail,re_ask=ask1,re_user=user1,re_time=retime)
        r1.save()  # 普通数据和外键插入的数据先save
        if r1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500

        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#添加回答的点赞
@api_view(['POST'])
def addreply_like(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        relike_username = request.data.get('username')
        re_id=request.data.get('replyid')
        user1 = UserInfo.maneger.get(username=relike_username)  # 现在User表中查询出前端选中的用户对应对象
        #ask1=AskInfo.maneger.get(id=reaskid)#找出对应id的问题表对象
        r1 = ReplyInfo.maneger.get(id=re_id)
        r1.re_like.add(user1)
        r1.save()  # 普通数据和外键插入的数据先save
        if r1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500

        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#取消点赞
@api_view(['POST'])
def delete_relike(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        delete_good_username = request.data.get('username')
        re_id = request.data.get('replyid')

        user1 = UserInfo.maneger.get(username=delete_good_username)   #获取到将要取消的对象
        r1 = ReplyInfo.maneger.get(id=re_id)#获取到对应回复下的将要减1赞的回复对象
        r1.re_like.remove(user1)
        if r1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#添加回答的踩
@api_view(['POST'])
def addreply_bad(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        relike_username = request.data.get('username')
        re_id=request.data.get('replyid')
        user1 = UserInfo.maneger.get(username=relike_username)  # 现在User表中查询出前端选中的用户对应对象
        #ask1=AskInfo.maneger.get(id=reaskid)#找出对应id的问题表对象
        r1 = ReplyInfo.maneger.get(id=re_id)
        r1.re_bad.add(user1)
        r1.save()  # 普通数据和外键插入的数据先save
        if r1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500

        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#取消踩
@api_view(['POST'])
def delete_rebad(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        delete_good_username = request.data.get('username')
        re_id = request.data.get('replyid')

        user1 = UserInfo.maneger.get(username=delete_good_username)   #获取到将要取消的对象
        r1 = ReplyInfo.maneger.get(id=re_id)#获取到对应回复下的将要减1赞的回复对象
        r1.re_bad.remove(user1)
        if r1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#展示所有问题
@api_view(['POST'])
def showask(request):
    context = {'status': 400,'content':'null'}
    if request.method == "POST":
        # 获取到对象，之后序列化
        ask_list=AskInfo.maneger.all().values_list('ask_title','ask_details','ask_user__username','ask_time',)#'ask_details','ask_user','ask_time')
        ask_list1=convert_to_json_string_2(ask_list)
        #ask_list=AskInfo.maneger.get(ask_user__username='li')
        #ask_list1=AskSerializer(ask_list)
        return HttpResponse(ask_list1)
    return HttpResponse(JSONRenderer().render(context))
#所有问题json输出格式
def convert_to_json_string_2(data):
    #label11=[]
    #for i in data:
        #ask11=AskInfo.maneger.get(ask_title=i[0])
        #label11=ask11.ask_label.get("askinfo__ask_label")
        return json.dumps({'ask':
                           [{'title': i[0],
                             'details': i[1],
                             'askuser':i[2],
                             'asktime':i[3],

                            #'asklable':i[4],
                             } for i in data]}, indent=4)

#展示所有标签
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
#标签输出形式json格式
def convert_to_json_string_label(data):
    return json.dumps({'label':
                           [{'labelid': i[0],
                             'labeltitle': i[1],
                             } for i in data]}, indent=4)

#查询我提出的问题
@api_view(['POST'])
def myask(request):
    context = {'status': 400, 'content': "null"}
    if request.method == "POST":
        username = request.data.get('username')
        try:
            u=UserInfo.maneger.get(username=username)
            ask = AskInfo.maneger.filter(ask_user=u)
            #ask1=ask.values_list()
            #ask=AskInfo.maneger.filter(ask_user__username=username)
            # 查询集为空时候
            if ask.count() != 0:
                context['status'] = 200
                #serialize=AskSerializer(ask)
                #content = JSONRenderer().render(serialize.data)
                serialize = serializers.serialize("json",ask)#,use_natural_keys=True)
                # 这里先将json对象转化为列表进行存储缺少这一步的话将无法解析。
                context['content'] = json.loads(serialize)
        except Exception:
            context['status'] = 500
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#查询我关注的标签
@api_view(['POST'])
def mylabel(request):
    # 考虑到出错的可能性，一开始就设置为
    context = {'status': 400, 'content': 'null'}
    if request.method == "POST":
        username = request.data.get('username', )
        #password = request.data.get('password')
        try:
            user = UserInfo.maneger.get(username=username)
            if user:
                context['status'] = 200
        except:
            context['status'] = 400
        if context['status'] == 200:
            serializer = MylabelSerializer(user)
            context['content'] = serializer.data
        else:
            context['content'] = "null"
       # content = JSONRenderer().render(serializer.data)
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#根据该问题展示问题的详情
@api_view(['POST'])
def theask(request):
    # 考虑到出错的可能性，一开始就设置为
    context = {'status': 400, 'content': 'null'}
    if request.method == "POST":
        asktitle = request.data.get('asktitle', )
        #password = request.data.get('password')
        try:
            theask = AskInfo.maneger.get(ask_title=asktitle)
            if theask:
                context['status'] = 200
        except:
            context['status'] = 400
        if context['status'] == 200:
            serializer = AskSerializer(theask)
            context['content'] = serializer.data
        else:
            context['content'] = "null"
        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content)
    return HttpResponse(JSONRenderer().render(context))

#删除我关注的标签
@api_view(['POST'])
def delete_theask(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        asktitle = request.data.get('asktitle', )

        a1 = AskInfo.maneger.filter(ask_title=asktitle)   #获取到将要取消的对象
        a1.delete()
        context['status'] = 200
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#根据该回复展示回复详情
@api_view(['POST'])
def thereply(request):
    # 考虑到出错的可能性，一开始就设置为
    context = {'status': 400, 'content': 'null'}
    if request.method == "POST":
        replyid = request.data.get('replyid', )
        #password = request.data.get('password')
        try:
            thereply = ReplyInfo.maneger.get(id=replyid)
            if thereply:
                context['status'] = 200
        except:
            context['status'] = 400
        if context['status'] == 200:
            serializer = ReplySerializer(thereply)
            context['content'] = serializer.data
        else:
            context['content'] = "null"
        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content)
    return HttpResponse(JSONRenderer().render(context))

#删除我关注的标签
@api_view(['POST'])
def delete_thereply(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        replyid = request.data.get('replyid', )

        r1 = ReplyInfo.maneger.filter(id=replyid)   #获取到将要取消的对象
        r1.delete()
        context['status'] = 200
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))


#查询当前标签下的问题
@api_view(['POST'])
def label_ask(request):
    context = {'status': 400, 'content': "null"}
    if request.method == "POST":
        label = request.data.get('label')
        l=LabelInfo.maneger.get(lb_title=label)
        label_asklist = AskInfo.maneger.filter(ask_label=l)
        if label_asklist.count() != 0:
            label_asklist = label_asklist.values_list('ask_title','ask_user__username', 'ask_details','ask_time')
            context['status'] = 200
            label_asklist1 = convert_to_json_string_lael_ask(label_asklist,context['status'])
            return HttpResponse(label_asklist1)
        else:
            context['status'] = 300
    return HttpResponse(JSONRenderer().render(context))

def convert_to_json_string_lael_ask(data,status):
    return json.dumps({'label_ask':
                           [{'asktitle': i[0],
                             'askuser': i[1],
                             'askdetails': i[2],
                             'asktime': i[3],
                             } for i in data], 'status':status}, indent=4)


#给用户添加关注的标签
@api_view(['POST'])
def adduser_label(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        username = request.data.get('username')
        userlabel = request.data.get('userlabel')
        try:
            user1=UserInfo.maneger.get(username=username)#现在User表中查询出前端选中的用户对应对象
            l1 = LabelInfo.maneger.get(lb_title=userlabel)
            user1.user_label.add(l1)
            if user1:
                context['status'] = 200  # 全保存
            else:
                context['status'] = 300  # 标签未保存
        except:
            context['status'] = 0
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#删除我关注的标签
@api_view(['POST'])
def delete_userlabel(request):
    context = {'status': 400}
    if request.method == "POST":
        # 获取到对象，之后序列化
        dellabel = request.data.get('dellabel')
        username = request.data.get('username')

        user1 = UserInfo.maneger.get(username=username)   #获取到将要取消的对象
        l1 = LabelInfo.maneger.get(lb_title=dellabel)#获取到对应回复下的将要减1赞的回复对象
        user1.user_label.remove(l1)
        if user1:
            #r2=ReplyInfo.maneger.filter(re_ask=user1)
            #r2.re_user.add(reuser)
            context['status'] = 200
        else:
            context['status']=500
        return HttpResponse(JSONRenderer().render(context))
    return HttpResponse(JSONRenderer().render(context))

#根据该问题展示问题的回答详情
@api_view(['POST'])
def theask_reply(request):
    context = {'status': 400, 'content': "null"}
    if request.method == "POST":
        asktitle = request.data.get('asktitle')
        replylist = ReplyInfo.maneger.filter(re_ask__ask_title=asktitle)
            # theask = AskInfo.maneger.get(ask_title=asktitle)
        if replylist.count() != 0:
            replylist=replylist.values_list('re_ask__ask_title', 're_user__username', 're_details', 're_time','id')
            context['status'] = 200
            replylist1 = convert_to_json_string_relist(replylist,context['status'])
            #context['content']=replylist1
            return HttpResponse(replylist1,JSONRenderer().render(context))
        else:
            context['status'] = 300
    return HttpResponse(JSONRenderer().render(context))
def convert_to_json_string_relist(data,status):
    return json.dumps({'the_reply':
                           [{'replyask': i[0],
                             'replyuser': i[1],
                             'redetails':i[2],
                             'retime':i[3],
                             'reid':i[4],
                             } for i in data], 'status':status}, indent=4)

#我回答过的问题
@api_view(['POST'])
def myreply(request):
    context = {'status': 400, 'content': "null"}
    if request.method == "POST":
        username = request.data.get('username')
        myreplylist = ReplyInfo.maneger.filter(re_user__username=username)
        # theask = AskInfo.maneger.get(ask_title=asktitle)
        if myreplylist.count() != 0:
            myreplylist = myreplylist.values_list('id','re_ask__ask_title','re_details', 're_time')
            context['status'] = 200
            myreplylist1 = convert_to_json_string_myrelist(myreplylist,context['status'])
            return HttpResponse(myreplylist1)
        else:
            context['status'] = 300
    return HttpResponse(JSONRenderer().render(context))
def convert_to_json_string_myrelist(data,status):
    return json.dumps({'myreply':
                           [{'replyid':i[0],
                             'replyask': i[1],
                             'replydetail': i[2],
                             'replytime': i[3],

                             } for i in data], 'status':status}, indent=4)

#我的问题新回答通知
@api_view(['POST'])
def myask_reinform(request):
    context = {'status': 400, 'content': "null"}
    if request.method == "POST":
        username = request.data.get('username')
        myask_replylist = ReplyInfo.maneger.filter(re_ask__ask_user__username=username)
        # theask = AskInfo.maneger.get(ask_title=asktitle)
        if myask_replylist.count() != 0:
            myask_replylist = myask_replylist.values_list('id','re_ask__ask_title','re_user__username','re_time')
            context['status'] = 200
            myask_replylist1 = convert_to_json_string_myask_reinform(myask_replylist,context['status'])
            return HttpResponse(myask_replylist1)
        else:
            context['status'] = 300
    return HttpResponse(JSONRenderer().render(context))
def convert_to_json_string_myask_reinform(data,status):
    return json.dumps({'myask_reinfo':
                           [{'re_infoid':i[0],
                             're_infoask': i[1],
                             're_infousr': i[2],
                             're_infotime': i[3],
                             } for i in data], 'status':status}, indent=4)



#根据用户id展示用户的详情
@api_view(['POST'])
def theuser(request):
    # 考虑到出错的可能性，一开始就设置为
    context = {'status': 400, 'content': 'null'}
    if request.method == "POST":
        userid = request.data.get('userid', )
        #password = request.data.get('password')
        try:
            theuser = UserInfo.maneger.get(id=userid)
            if theuser:
                context['status'] = 200
        except:
            context['status'] = 400
        if context['status'] == 200:
            serializer = UserSerializer(theuser)
            context['content'] = serializer.data
        else:
            context['content'] = "null"
        content = JSONRenderer().render(serializer.data)
        return HttpResponse(content)
    return HttpResponse(JSONRenderer().render(context))
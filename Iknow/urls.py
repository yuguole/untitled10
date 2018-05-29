from django.urls import path, include
from Iknow import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),#登录
    # 注册的路由 POST
    path('register', views.register, name='register'),#注册
    path('addask', views.addask, name='addask'),#添加新问题
    path('addlabel',views.addlabel,name='addlabel'),#添加新标签
    path('addreply',views.addreply,name='addreply'),#添加新回答
    path('showask',views.showask,name='showask'),#展示所有问题
    path('showlabel', views.showlabel, name='showlabel'),#展示所有标签
    path('myask', views.myask, name='myask'),#展示我提出的问题
    path('mylabel', views.mylabel, name='mylabel'),#展示我关注的标签
    path('theask',views.theask,name='theask'),#该问题详情
    path('label_ask',views.label_ask,name='label_ask'),#该标签下的问题
    path('adduser_label',views.adduser_label,name='adduser_label'),#添加关注的标签
    path('theask_reply',views.theask_reply,name='theask_reply'),#该问题下的回复
    path('myreply',views.myreply,name='myreply'),#我回复的问题
    path('theuser',views.theuser,name='theuser'),#该用户详情
    path('thereply',views.thereply,name='thereply'),#该回复详情
    path('myask_reinform',views.myask_reinform,name='myask_reinform'),#我提出的问题回复通知
    path('delete_relike',views.delete_relike,name='delete_relike'),#取消点赞
    path('addreply_like',views.addreply_like,name='addreply_like'),#添加点赞人数
    path('delete_rebad',views.delete_rebad,name='delete_rebad'),#取消踩
    path('addreply_bad',views.addreply_bad,name='addreply_bad'),#添加踩
]
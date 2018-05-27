from django.urls import path, include
from Iknow import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    # 注册的路由 POST
    path('register', views.register, name='register'),
    path('addask', views.addask, name='addask'),
    path('addlabel',views.addlabel,name='addlabel'),
    path('addreply',views.addreply,name='addreply'),
    path('showask',views.showask,name='showask'),
    path('showlabel', views.showlabel, name='showlabel'),
    path('myask', views.myask, name='myask'),
    path('mylabel', views.mylabel, name='mylabel'),
    path('theask',views.theask,name='theask'),
    path('label_ask',views.label_ask,name='label_ask'),
    path('adduser_label',views.adduser_label,name='adduser_label'),
    path('theask_reply',views.theask_reply,name='theask_reply'),
    path('myreply',views.myreply,name='myreply'),
    path('theuser',views.theuser,name='theuser'),
    path('thereply',views.thereply,name='thereply'),

]
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

]
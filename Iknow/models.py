from django.db import models

from rest_framework.serializers import ModelSerializer
# Create your models here.
class UserManager(models.Manager):
    def create(self, username, password,):
        user = UserInfo()
        user.username = username
        user.password = password
        return user

class UserInfo(models.Model):
    GENDER_CHOICES=(
        (u'f',u'男'),(u'm',u'女')
    )
    username=models.CharField(max_length=128,unique=True)
    password=models.CharField(max_length=256)
    #email=models.EmailField(unique=True)
    sex=models.CharField(max_length=2,choices=GENDER_CHOICES,default="男")
    user_date=models.DateField(blank=True,auto_now_add=True)#用户出身年月
    #一个用户可以关注多个标签，一个标签可以有多个用户
    user_label=models.ManyToManyField('LabelInfo',blank=True)
    def __str__(self):
        return self.username
    maneger = UserManager()

class AskInfo(models.Model):
    ask_title=models.CharField(max_length=128)      #问题标题
    ask_time=models.DateTimeField(auto_now_add=True)         #问题时间,创建时自动更新当前时间
    ask_details=models.CharField(max_length=600,blank=True)    #问题详细内容
    ask_user=models.ForeignKey('UserInfo',on_delete=models.CASCADE)#设置外键对应用户表的主键
    #一个问题可以包含多个标签，一个标签可以包含多个问题
    ask_lable=models.ManyToManyField('LabelInfo')
    def __str__(self):
        return self.ask_title

class ReplyInfo(models.Model):
    re_details=models.TextField()
    re_time=models.DateTimeField(auto_now_add=True)
    re_ask=models.ForeignKey('askInfo',on_delete=models.CASCADE)#一个问题可以有多个回答
    #re_User=models.ManyToManyField('UserInfo')#一个问题可以有多个用户回答，也一个用户可以回答多个问题
    class Meta:
        abstract=True

class CommentInfo(models.Model):
    com_details=models.CharField(max_length=3000)
    com_time=models.DateTimeField(auto_now_add=True)
    #一个回答可以有多个评论
    com_reply=models.ForeignKey('ReplyInfo',on_delete=models.CASCADE)
    #一个用户可以评论多个回答，一个回答也可以有多个用户评论
    #com_user=models.ManyToManyField('UserInfo')
    class Meta:
        abstract=True


class LabelInfo(models.Model):
    lb_title=models.CharField(max_length=20)
    def __str__(self):
        return self.lb_title
    #一个标签可以有多个用户关注，一个用户也可以关注多个标签
    lb_user=models.ManyToManyField('UserInfo')
    #标签和问题是多对多关系
    lb_ask=models.ManyToManyField('AskInfo')
#迁移完了之后，还没有添加数据等



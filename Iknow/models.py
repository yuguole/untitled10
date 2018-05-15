from django.db import models

from rest_framework.serializers import ModelSerializer
# Create your models here.
class UserManager(models.Manager):
    def get_by_natural_key(self, username, password,):
        return self.get(username=username, password=password)
    def create(self, username, password,):
        user = UserInfo()
        user.username = username
        user.password = password
        return user

class AskManager(models.Manager):
    def create(self,asktitle, askdetail):
        ask=AskInfo()
        #ask.ask_user=username
        ask.ask_title=asktitle
        ask.ask_details=askdetail
        return ask

class LabelManager(models.Manager):
    def get_by_natural_key(self, lb_title):
        return self.get(lb_title=lb_title)
    def create(self,lb_title):
        label=LabelInfo()
        label.lb_title=lb_title
        return label

class ReplyManager(models.Manager):
    def create(self,redetails,reuser):
        re=ReplyInfo()
        #re.re_ask=reask
        re.re_details=redetails
        re.re_user=reuser
        return re

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
    ask_title=models.CharField(max_length=128,unique=True)      #问题标题
    ask_time=models.CharField(max_length=60)         #问题时间,创建时从前台获取当前时间
    ask_details=models.CharField(max_length=600,blank=True,default='如题')    #问题详细内容
    ask_user=models.ForeignKey('UserInfo', related_name='myasks',on_delete=models.CASCADE)#设置外键对应用户表的主键
    #一个问题可以包含多个标签，一个标签可以包含多个问题
    ask_label=models.ManyToManyField('LabelInfo',blank=True,)
    class Meta:
        ordering = ['-ask_time']  # 减号代表倒序排列
    def __str__(self):
        return self.ask_title
    maneger =AskManager()





class ReplyInfo(models.Model):
    #re_comment=models.ForeignKey('CommentInfo',on_delete=models.DO_NOTHING)#可
    re_ask = models.ForeignKey('AskInfo', on_delete=models.CASCADE)  # 一个问题可以有多个回答,删除问题同时删除回答
    re_details=models.TextField()
    re_time=models.CharField(max_length=60)
    re_user=models.ForeignKey('UserInfo',on_delete=models.CASCADE)#一个回答对应一个用户，也一个用户可以对应多个回答
    def __str__(self):
        return self.re_details
    class Meta:
        ordering=['-re_time']
    maneger=ReplyManager()

class CommentInfo(models.Model):
    com_details=models.CharField(max_length=3000)
    com_time=models.CharField(max_length=60)
    #一个回答可以有多个评论
    com_reply=models.ForeignKey('ReplyInfo',on_delete=models.CASCADE)
    #一个用户可以评论多个回答，一个回答也可以有多个用户评论
    #com_user=models.ManyToManyField('UserInfo')
    class Meta:
        abstract=True
        ordering=['-com_time']


class LabelInfo(models.Model):

    lb_title=models.CharField(max_length=20,unique=True)

    def natural_key(self):
        return (self.lb_title)
    def __str__(self):
        return self.lb_title
    maneger = LabelManager()
#迁移完了之后，还没有添加数据等



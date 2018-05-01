from django.contrib import admin
from .models import*

class UserInfoAdmin(admin.ModelAdmin):#(admin.ModelAdmin):
    list_display = ['id','username','password','sex','user_date']
    list_filter = ['sex']

class AskInfoAdmin(admin.ModelAdmin):
    list_display = ['id','ask_title','ask_details','ask_user','ask_time']
    list_filter = ['ask_label']

class ReplyInfoAdmin(admin.ModelAdmin):
    list_display = ['id','re_ask','re_details','re_user','re_time']
    list_filter = ['re_ask']

class LabelInfoAdmin(admin.ModelAdmin):
    list_display = ['id','lb_title']


# Register your models here.
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(AskInfo,AskInfoAdmin)
admin.site.register(ReplyInfo,ReplyInfoAdmin)
#admin.site.register(CommentInfo)
admin.site.register(LabelInfo,LabelInfoAdmin)

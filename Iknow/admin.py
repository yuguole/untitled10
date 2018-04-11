from django.contrib import admin
from .models import*

class UserInfoAdmin(admin.ModelAdmin):#(admin.ModelAdmin):
    list_display = ['id','username','password','sex','user_date']
    list_filter = ['sex']


# Register your models here.
admin.site.register(UserInfo,UserInfoAdmin)
admin.site.register(AskInfo)
#admin.site.register(ReplyInfo)
#admin.site.register(CommentInfo)
admin.site.register(LabelInfo)

from rest_framework import serializers

import json
from datetime import date
from datetime import datetime

from rest_framework.serializers import ModelSerializer
from rest_framework.templatetags.rest_framework import data
from rest_framework.utils import json

from Iknow.models import*




# dl= json.dumps(datalist, cls=JsonCustomEncoder)




class UserSerializer(serializers.ModelSerializer):
    #user_label = LabelSerializer()
    #myasks = AskSerializer(many=True,read_only=True)
    # 设置序列化
    class Meta:
        model = UserInfo
        fields = "__all__"
        #depth = 1
        #fields =('username','password','myasks')

class LabelSerializer(serializers.ModelSerializer):

    class Meta:
        model=LabelInfo
        fields="__all__"

class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model=AskInfo
        fields="__all__"
        depth=1


class ReplySerializer(ModelSerializer):
    class Meta:
        model=ReplyInfo
        fields="__all__"

class MylabelSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserInfo
        fields = ( 'id','user_label')
        depth=1



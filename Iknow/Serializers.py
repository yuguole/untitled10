from rest_framework.serializers import ModelSerializer
from Iknow.models import*
from marshmallow import Schema, fields

class UserSerializer(ModelSerializer):
    # 设置序列化
    class Meta:
        model = UserInfo
        fields = "__all__"

class LabelSerializer(ModelSerializer):
    class Meta:
        model=LabelInfo
        fields="__all__"

class AskSerializer(ModelSerializer):
    class Meta:
        model=AskInfo
        fields="__all__"

class ReplySerializer(ModelSerializer):
    class Meta:
        model=ReplyInfo
        fields="__all__"



from rest_framework.serializers import ModelSerializer
from Iknow.models import UserInfo

class UserSerializer(ModelSerializer):
    # 设置序列化
    class Meta:
        model = UserInfo
        fields = "__all__"
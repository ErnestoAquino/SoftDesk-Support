from rest_framework.serializers import ModelSerializer

from user_contrib_app.models import CustomUser


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "age", "can_be_contacted", "can_data_be_shared"]

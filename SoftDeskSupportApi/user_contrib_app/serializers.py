from rest_framework.serializers import ModelSerializer

from user_contrib_app.models import CustomUser
from user_contrib_app.models import Contributor


class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "age", "can_be_contacted", "can_data_be_shared"]


class ContributorSerializer(ModelSerializer):

    user = CustomUserSerializer()

    class Meta:
        model = Contributor
        fields = ["id", "user", "project"]

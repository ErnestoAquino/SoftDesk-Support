from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.serializers import HyperlinkedRelatedField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import CharField

from user_contrib_app.models import CustomUser
from user_contrib_app.models import Contributor
from project_management_app.models import Project


class CustomUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "age", "can_be_contacted", "can_data_be_shared"]

    def create(self, validated_data):
        can_be_contacted = validated_data.get('can_be_contacted', False)
        can_data_be_shared = validated_data.get('can_data_be_shared', False)

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            age=validated_data['age'],
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ContributorSerializer(ModelSerializer):

    # user = PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    user = SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    # project = PrimaryKeyRelatedField(queryset=Project.objects.all())
    project = HyperlinkedRelatedField(view_name="projects-detail",
                                      queryset=Project.objects.all(),
                                      lookup_field="pk")

    class Meta:
        model = Contributor
        fields = ["user", "project"]

    # def validate(self, data):
    #     # Check if a Contributor with the same user and project already exists
    #     if Contributor.objects.filter(user=data["user"], project=data["project"]).exists():
    #         raise ValidationError({
    #             "non_field_errors": ["This user is already a contributor to this project."]
    #         })
    #     return data

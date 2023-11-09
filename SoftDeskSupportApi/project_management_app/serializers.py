from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from project_management_app.models import Project
from project_management_app.models import Issue
from project_management_app.models import Comment
from user_contrib_app.serializers import CustomUserSerializer


class AuthorSerializerMixin(serializers.Serializer):
    author = serializers.SerializerMethodField()

    def get_author(self, instance):
        if instance.author.can_data_be_shared:
            serializer = CustomUserSerializer(instance.author)
            return serializer.data
        else:
            return {}


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description"]


class ProjectDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    contributors = CustomUserSerializer(many = True)

    class Meta:
        model = Project
        fields = ("id", "name", "description", "type", "created_time", "author", "contributors")


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "description", "status", "priority", "tag"]


class IssueDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    # author = serializers.SerializerMethodField()
    project = ProjectDetailSerializer(read_only = True)

    class Meta:
        model = Issue
        fields = ("id", "title", "description", "status", "priority", "tag", "project", "assignee", "author")

    # def get_author(self, instance):
    #     if instance.author.can_data_be_shared:
    #         serializer = CustomUserSerializer(instance.author)
    #         return serializer.data
    #     else:
    #         return {}


class CommentDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    issue = IssueDetailSerializer()

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue"]


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description"]

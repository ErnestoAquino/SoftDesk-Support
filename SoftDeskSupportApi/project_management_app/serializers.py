from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
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
    url = HyperlinkedIdentityField(view_name="projects-detail", read_only = True)

    class Meta:
        model = Project
        fields = ["url", "name", "description", "type"]


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
    project = ProjectDetailSerializer(read_only = True)

    class Meta:
        model = Issue
        fields = ("id", "title", "description", "status", "priority", "tag", "project", "assignee", "author")


class CommentDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    issue = IssueDetailSerializer()

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue"]


class CommentListSerializer(ModelSerializer):
    issue = HyperlinkedRelatedField(view_name = "issues-detail",
                                    queryset = Issue.objects.all(),
                                    lookup_field = "pk")

    class Meta:
        model = Comment
        fields = ["id", "description", "author", "issue"]

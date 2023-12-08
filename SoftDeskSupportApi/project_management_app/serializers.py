from rest_framework.relations import HyperlinkedRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import HyperlinkedIdentityField
from rest_framework.serializers import SlugRelatedField
from rest_framework.serializers import CharField
from rest_framework import serializers
from project_management_app.models import Project
from project_management_app.models import Issue
from project_management_app.models import Comment
from project_management_app.models import CustomUser
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
    url = HyperlinkedIdentityField(view_name="projects-detail", read_only=True)

    class Meta:
        model = Project
        fields = ["url", "name", "description", "type"]


class IssueListSerializer(ModelSerializer):
    assignee = SlugRelatedField(slug_field="username",
                                queryset=CustomUser.objects.all(),
                                required=False,
                                allow_null=True)

    class Meta:
        model = Issue
        fields = ["id", "title", "description", "status", "priority", "tag", "assignee"]

    def validate_assignee(self, value):
        # Retrieve the project from the context
        project = self.context.get("project")
        if not project:
            raise serializers.ValidationError("Project context is missing.")

        # Check if the assignee is a contributor of the project
        if value and value not in project.contributors.all():
            raise serializers.ValidationError("The assigned user must be a contributor of the project.")
        return value


class ProjectDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    author_username = CharField(source='author.username', read_only=True)
    issues = SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
    contributors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Project
        fields = ("id", "name", "description", "type", "created_time", "author_username", "issues", "contributors")


class IssueDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    assignee = serializers.SlugRelatedField(slug_field='username', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Issue
        fields = ("id", "title", "description", "status", "priority", "tag", "project", "assignee", "author")


class CommentDetailSerializer(ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "description", "author_username", "created_time"]


class CommentListSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "description"]

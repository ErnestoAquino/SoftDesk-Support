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
    """
    A mixin serializer to include author information based on user's data sharing preferences.
    """
    author = serializers.SerializerMethodField()

    def get_author(self, instance):
        """
        Returns author data if they opted to share it; otherwise returns an empty dictionary.
        """
        if instance.author.can_data_be_shared:
            serializer = CustomUserSerializer(instance.author)
            return serializer.data
        else:
            return {}


class ProjectListSerializer(ModelSerializer):
    """
    Serializer for listing projects with a URL to detailed view.
    """
    url = HyperlinkedIdentityField(view_name="projects-detail", read_only=True)

    class Meta:
        model = Project
        fields = ["url", "name", "description", "type"]


class IssueListSerializer(ModelSerializer):
    """
    Serializer for listing issues, including assigned user information.
    """
    assignee = SlugRelatedField(slug_field="username",
                                queryset=CustomUser.objects.all(),
                                required=False,
                                allow_null=True)

    class Meta:
        model = Issue
        fields = ["id", "title", "description", "status", "priority", "tag", "assignee"]

    def validate_assignee(self, value):
        """
        Validates that the assignee is a contributor to the project.
        """
        # Retrieve the project from the context
        project = self.context.get("project")
        if not project:
            raise serializers.ValidationError("Project context is missing.")

        # Check if the assignee is a contributor of the project
        if value and value not in project.contributors.all():
            raise serializers.ValidationError("The assigned user must be a contributor of the project.")
        return value


class ProjectDetailSerializer(AuthorSerializerMixin, ModelSerializer):
    """
    Detailed serializer for projects, including author, issues, and contributors.
    """
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
    """
    Detailed serializer for issues, including project, assignee, and author information.
    """
    project = serializers.SlugRelatedField(slug_field='name', read_only=True)
    assignee = serializers.SlugRelatedField(slug_field='username', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Issue
        fields = ("id", "title", "description", "status", "priority", "tag", "project", "assignee", "author")


class CommentDetailSerializer(ModelSerializer):
    """
    Detailed serializer for comments, including author's username and creation time.
    """
    author_username = serializers.CharField(source="author.username", read_only=True)
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "description", "author_username", "created_time"]


class CommentListSerializer(ModelSerializer):
    """
    Basic serializer for listing comments.
    """
    class Meta:
        model = Comment
        fields = ["id", "description"]

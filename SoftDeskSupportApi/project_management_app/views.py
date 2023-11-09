from rest_framework.viewsets import ModelViewSet

from project_management_app.models import Project
from project_management_app.models import Issue
from project_management_app.models import Comment
from project_management_app.serializers import ProjectListSerializer
from project_management_app.serializers import ProjectDetailSerializer
from project_management_app.serializers import IssueListSerializer
from project_management_app.serializers import IssueDetailSerializer
from project_management_app.serializers import CommentListSerializer
from project_management_app.serializers import CommentDetailSerializer


class BaseViewSet(ModelViewSet):
    detail_serializer_class = None

    def get_serializer_class(self):
        """
        Use `detail_serializer_class` for 'retrieve' action or default to
        `serializer_class` for other actions.
        """
        if self.action == "retrieve" and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        return Issue.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()


class CommentViewSet(BaseViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        return Comment.objects.all()

from rest_framework.viewsets import ModelViewSet

from project_management_app.models import Project
from project_management_app.models import Issue
from project_management_app.models import Comment
from project_management_app.serializers import ProjectSerializer
from project_management_app.serializers import IssueSerializer
from project_management_app.serializers import CommentSerializer


class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()


class IssueViewSet(ModelViewSet):
    serializer_class = IssueSerializer

    def get_queryset(self):
        return Issue.objects.all()


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()

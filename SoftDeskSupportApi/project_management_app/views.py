from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from project_management_app.permissions import IsAuthor
from project_management_app.permissions import IsContributor
from project_management_app.models import Project
from project_management_app.models import Issue
from project_management_app.models import Comment
from project_management_app.serializers import ProjectListSerializer
from project_management_app.serializers import ProjectDetailSerializer
from project_management_app.serializers import IssueListSerializer
from project_management_app.serializers import IssueDetailSerializer
from project_management_app.serializers import CommentListSerializer
from project_management_app.serializers import CommentDetailSerializer
from user_contrib_app.models import Contributor


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

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsAuthor)
        if self.action in ['retrieve', 'list']:
            permission_classes.append(IsContributor)
        permission_instances = []
        for permission in permission_classes:
            permission_instances.append(permission())
        return permission_instances

    def get_queryset(self):
        return Project.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)
        return Response(serializer.data, status = status.HTTP_201_CREATED)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return Issue.objects.filter(project__contributors = self.request.user)
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

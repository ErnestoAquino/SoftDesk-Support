from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from project_management_app.permissions import IsProjectAuthor
from project_management_app.permissions import IsProjectContributor
from project_management_app.permissions import HasProjectAccessPermission
from project_management_app.permissions import IsIssueAuthor
from project_management_app.permissions import IsContributorToProjectOfIssue
from project_management_app.permissions import IsCommentAuthor
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
            permission_classes.append(IsProjectAuthor)
        if self.action in ['retrieve', 'list']:
            permission_classes.append(IsProjectContributor)
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
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssueViewSet(ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, HasProjectAccessPermission]

    def get_queryset(self):
        project_pk = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=project_pk)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        permissions = super().get_permissions()

        if self.action in ['destroy', 'update', 'partial_update']:
            permissions = [IsIssueAuthor()]
        return permissions

    def create(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])

        # Only the author or contributors of the project can create issues
        if request.user != project.author and request.user not in project.contributors.all():
            raise PermissionDenied("Only the author or contributors can create issues.")

        serializer = self.get_serializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Retrieve the associated project using the project ID from the URL
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        # Get the specific issue instance to be updated
        instance = self.get_object()

        # Initialize the serializer for a full update (PUT)
        serializer = self.get_serializer(instance, data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated instance

        return Response(serializer.data)  # Return the serialized data of the updated instance

    def partial_update(self, request, *args, **kwargs):
        # Retrieve the associated project using the project ID from the URL
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        # Get the specific issue instance to be updated
        instance = self.get_object()

        # Initialize the serializer for a partial update (PATCH)
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'project': project})
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated instance

        return Response(serializer.data)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentListSerializer
    detail_serializer_class = CommentDetailSerializer

    def get_queryset(self):
        # Extract the issue ID from the URL parameters
        issue_pk = self.kwargs.get('issue_pk')

        # Filter the comments that belong to the specified issue
        return Comment.objects.filter(issue=issue_pk)

    def get_permissions(self):
        # Adds IsAuthenticated for all actions
        permission_classes = [IsAuthenticated]

        # Adds custom permission for specific actions
        if self.action in ["list", "create", "retrieve"]:
            permission_classes.append(IsContributorToProjectOfIssue)
        elif self.action in ["update", "partial_update", "destroy"]:
            permission_classes.append(IsCommentAuthor)
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Extract issue ID from URL and retrieve the corresponding issue object, raising 404 if not found
        issue_pk = self.kwargs.get('issue_pk')
        issue = get_object_or_404(Issue, pk=issue_pk)

        # Initialize serializer with request data, validate it, and save the new comment with issue and author
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(issue=issue, author=request.user)

        # Return a 201 Created response with the serialized comment data
        return Response(serializer.data, status=status.HTTP_201_CREATED)

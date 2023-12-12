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


class ProjectViewSet(BaseViewSet):
    """
    Manages CRUD operations for projects in the application.

    Utilizes two serializers: one for listing projects and another for project details.
    Enables users to list, view details, create, update, and delete projects.
    """
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerializer

    def get_permissions(self):
        """
        Assigns permissions based on the action. Only the author of the project can modify or delete it.
        """
        permission_classes = [IsAuthenticated]

        # Only the author of the project can update or delete
        if self.action in ['update', 'partial_update', 'destroy']:
            permission_classes.append(IsProjectAuthor)
        if self.action in ['retrieve', 'list']:
            permission_classes.append(IsProjectContributor)
        permission_instances = []

        # Instantiate and return the permissions
        for permission in permission_classes:
            permission_instances.append(permission())
        return permission_instances

    def get_queryset(self):
        """
        Returns a queryset containing all projects.
        """
        return Project.objects.all()

    def perform_create(self, serializer):
        """
        Creates a new project. Automatically sets the user making the request as the author
        and contributor of the project.
        """
        # Save the project with the current user as the author
        project = serializer.save(author=self.request.user)
        # Automatically add the author as a contributor
        Contributor.objects.create(user=self.request.user, project=project)
        # Return the data of the created project
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class IssueViewSet(BaseViewSet):
    """
    Manages CRUD operations for issues associated with projects in the application.
    """
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer

    def get_queryset(self):
        """
        Returns a queryset of issues for a specific project identified by `project_pk`.
        """
        project_pk = self.kwargs['project_pk']
        return Issue.objects.filter(project_id=project_pk)

    def get_permissions(self):
        """
        Assigns custom permissions based on the action being performed.
        """
        permissions_classes = [IsAuthenticated]

        if self.action in ['list', 'retrieve', 'create']:
            permissions_classes.append(HasProjectAccessPermission)
        # Only the author of the issue can update or delete
        if self.action in ['destroy', 'update', 'partial_update']:
            permissions_classes.append(IsIssueAuthor)
        return [permission() for permission in permissions_classes]

    def create(self, request, *args, **kwargs):
        """
        Creates a new issue for a project. Only authors or contributors of the project can create issues.
        """
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])

        # Restrict issue creation to project's author or contributors
        if request.user != project.author and request.user not in project.contributors.all():
            raise PermissionDenied("Only the author or contributors can create issues.")

        # Validate and save the issue
        serializer = self.get_serializer(data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project, author=request.user)

        # Return the serialized data of the newly created issue
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Updates an issue. Retrieves the associated project and the specific issue instance to be updated.
        """
        # Retrieve the associated project using the project ID from the URL
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        # Get the specific issue instance to be updated
        instance = self.get_object()

        # Initialize and validate the serializer for a full update
        serializer = self.get_serializer(instance, data=request.data, context={'project': project})
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated instance

        return Response(serializer.data)  # Return the serialized data of the updated instance

    def partial_update(self, request, *args, **kwargs):
        """
        Partially updates an issue. Retrieves the associated project and the specific issue instance to be updated.
        """

        # Retrieve the associated project using the project ID from the URL
        project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        # Get the specific issue instance to be updated
        instance = self.get_object()

        # Initialize and validate the serializer for a partial update
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'project': project})
        serializer.is_valid(raise_exception=True)  # Validate the data
        serializer.save()  # Save the updated instance

        return Response(serializer.data)


class CommentViewSet(BaseViewSet):
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

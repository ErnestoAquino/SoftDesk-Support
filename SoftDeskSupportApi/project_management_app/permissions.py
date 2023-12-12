from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound

from project_management_app.models import Project
from project_management_app.models import Issue


class IsProjectAuthor(BasePermission):
    """
    Permission to allow only the author to modify or delete an object.
    This method verifies if the user attempting to modify or delete the object is its author.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user == obj.author:
            raise PermissionDenied("Only the author can modify or delete this project.")
        return True


class IsProjectContributor(BasePermission):
    """
    Permission to check if the user is either the author or a contributor of the project.
    This permission checks whether the user is the author or a contributor of the project
    and grants access accordingly
    """

    def has_object_permission(self, request, view, obj):
        # Check if the current user is the author of the project
        if request.user == obj.author:
            # Grant access if the user is the author
            return True

        # Check if the current user is a contributor to the project
        if obj.contributors.filter(id=request.user.id).exists():
            # Grant access if the user is a contributor
            return True

        # If the user is neither the author nor a contributor, deny access with a custom message
        raise PermissionDenied("You need to be a contributor or the author to access this project.")


class HasProjectAccessPermission (BasePermission):
    """
    Restricts project access to its author or contributors.
    his permission checks if the user is either the author or a contributor of the project.
    It retrieves the project_pk from the URL to identify the project.
    """
    def has_permission(self, request, view):
        # Retrieve the project_pk from the URL
        project_pk = view.kwargs['project_pk']

        # Retrieve the project instance using the project ID
        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            # Raise a NotFound error if the project does not exist
            raise NotFound("Project not found")

        # Determine if the user is the author or a contributor of the project
        is_author = request.user == project.author
        is_contributor = request.user in project.contributors.all()

        if is_author or is_contributor:
            return True

        if view.action in ['list', 'retrieve']:
            raise PermissionDenied("Only contributors of the project can access its resources.")
        if view.action == 'create':
            raise PermissionDenied("You cannot create issues for a project you are not contributing to.")
        return False


class IsIssueAuthor(BasePermission):
    """
    Permission to only allow authors of an issue to perform specific actions.
    delete, update, partial_update.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the current user is the author of the issue.
        if obj.author != request.user:
            if view.action == "destroy":
                # If the action is 'destroy' (DELETE), only the author can delete the issue.
                raise PermissionDenied("Only the author can delete this issue.")
            elif view.action in ["update", "partial_update"]:
                # If the action is 'update' (PUT) or 'partial_update' (PATCH),
                # only the author can modify the issue.
                raise PermissionDenied("Only the author can modify this issue.")
        # If the current user is the author, allow the action.
        return True


class IsContributorToProjectOfIssue(BasePermission):
    """
    Permission to check if the user is a contributor to the project of the issue.
    """

    def has_permission(self, request, view):
        # Extract the issue ID from the URL parameters
        issue_pk = view.kwargs.get('issue_pk')

        try:
            # Retrieve the issue and its related project
            issue = Issue.objects.get(pk=issue_pk)
        except Issue.DoesNotExist:
            raise NotFound(detail="The requested resource is not available or does not exist")

        # Check if the user is a contributor to the project
        is_contributor = issue.project.contributors.filter(pk=request.user.pk).exists()

        if not is_contributor:
            if view.action == "create":
                # Custom message for trying to add a comment without being a contributor
                raise PermissionDenied(detail="You cannot add comments to a project unless you "
                                              "are a contributor.")
            else:
                # General message for other actions.
                raise PermissionDenied(detail="Only the contributors of the project can access "
                                              "its resources.")

        return True


class IsCommentAuthor(BasePermission):
    """
    Permission to check if the user is the author of the comment.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the current user is the author of the comment.
        if obj.author != request.user:
            if view.action == 'destroy':
                # If the action is 'destroy' (DELETE), only the author can delete the comment.
                raise PermissionDenied(detail="Only the author can delete this comment.")
            elif view.action in ["update", "partial_update"]:
                # If the action is 'update' (PUT) or 'partial_update' only the author can modify the comment.
                raise PermissionDenied(detail="Only the author can modify this comment.")
        # If the current user is the author, permit the action
        return True

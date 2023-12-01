from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from project_management_app.exceptions import CustomAPIException
from project_management_app.models import Project


class IsAuthor(BasePermission):
    """Permission to allow only the author to modify or delete an object."""
    def has_object_permission(self, request, view, obj):
        if not request.user == obj.author:
            raise CustomAPIException("Only the author can modify or delete this project.")
        return True


class IsContributor(BasePermission):
    """Permission to allow contributors to access an object."""

    def has_object_permission(self, request, view, obj):
        # Checks if the user is the author of the project
        if request.user == obj.author:
            return True

        # Checks if the user is a contributor to the project
        if obj.contributors.filter(id=request.user.id).exists():
            return True

        raise CustomAPIException("You need to be a contributor or the author to access this project.")


class HasProjectAccessPermission (BasePermission):

    def has_permission(self, request, view):
        # Retrieve the project_pk from the URL
        project_pk = view.kwargs['project_pk']

        # Obtain the project using project_pk
        try:
            project = Project.objects.get(pk=project_pk)
        except Project.DoesNotExist:
            return False

        # Check if the current user is the author of the project or a contributor
        return request.user == project.author or request.user in project.contributors.all()


class IsIssueAuthor(BasePermission):
    """
    Custom permission to only allow authors of an issue to perform specific actions.

    This permission class restricts the ability to delete, update, or partially update an issue
    to only the author of that issue. It checks if the current user is the author and raises
    an appropriate error message if they are not.
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

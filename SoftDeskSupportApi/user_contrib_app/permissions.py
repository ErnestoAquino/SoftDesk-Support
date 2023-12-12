import re

from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from project_management_app.models import Project


class UserProfilePermission(BasePermission):
    """
    Permission that restricts users to only accessing and modifying their own profile data.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the request method is one of the safe methods (GET, HEAD, OPTIONS).
        # Safe methods are read operations that do not alter data.
        if request.method in SAFE_METHODS:
            # If the user making the request is not the same as the object (profile), deny access.
            if obj != request.user:
                raise PermissionDenied("You cannot access a profile that is not your own.")
            return True

        # For write operations (POST, PUT, PATCH, DELETE), ensure that the user making the request
        # is the same as the object (profile). If not, deny the appropriate operation with a custom message.
        if obj != request.user:
            if request.method == "DELETE":
                raise PermissionDenied("You cannot delete a user who is not you.")
            else:
                raise PermissionDenied("You cannot modify a user who is not you.")
        return True


class IsProjectContributor(BasePermission):
    """
    Permission to check if the requesting user is a contributor of the specified project.
    """
    def has_permission(self, request, view):
        # Extract the project ID from the URL parameters.
        project_pk = view.kwargs.get("project_pk")
        # Retrieve the project instance.
        project = Project.objects.filter(pk=project_pk).first()

        if not project:
            return False

        if request.user not in project.contributors.all():
            # Custom error message if the user is not a contributor of the project
            raise PermissionDenied("Only project contributors can access this information.")

        return True


class IsProjectAuthor(BasePermission):
    """
    Permission to check if the requesting user is the author of the specified project.
    """
    def has_permission(self, request, view):
        # Extract the project ID from the URL parameters.
        project_pk = view.kwargs.get("project_pk")
        # Retrieve the project instance.
        project = Project.objects.filter(pk=project_pk).first()

        if not project:
            return False

        if project.author != request.user:
            if request.method == "POST":
                # Custom error message for trying to add a contributor when not the author
                raise PermissionDenied("Only the project's author can add a new contributor.")
            elif request.method == "DELETE":
                # Custom error message for trying to delete a contributor when not the author
                raise PermissionDenied("Only the project's author can remove a contributor.")

        return True

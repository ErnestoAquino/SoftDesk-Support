import re

from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied

from project_management_app.models import Project


class UserProfilePermission(BasePermission):
    """
    Custom permission object that only allows users to edit their own data.
    """
    def has_object_permission(self, request, view, obj):
        # Reading is allowed for any request,
        # thus GET, HEAD, or OPTIONS requests are allowed.
        if request.method in SAFE_METHODS:
            return True

        # Writing is only allowed if the user making the request is the same as the object.
        if obj != request.user:
            if request.method == "DELETE":
                raise PermissionDenied("You cannot delete a user who is not you.")
            else:
                raise PermissionDenied("You cannot modify a user who is not you.")
        return True


class IsProjectAuthor(BasePermission):
    """
    Permission to allow only the author of a project to add or remove a contributor.
    """

    def has_permission(self, request, view):
        # Retrieve the project ID from the request data.
        project_id = request.data.get("project")

        # If no project_id is provided, deny permission with a message.
        if not project_id:
            raise PermissionDenied("Project ID is required.")

        # Try to fetch the project with the given ID.
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            # If the project does not exist, deny permission with a message.
            raise PermissionDenied("Project does not exist.")

        # Check if the user making the request is the author of the project.
        if project.author != request.user:
            # If the user is not the author, deny permission with a message.
            raise PermissionDenied("You do not have permission to add contributors to this project.")
        # If all checks pass, grant permission.
        return True


class IsProjectAuthorTest(BasePermission):
    def has_permission(self, request, view):

        if request.method == "DELETE":
            project_url = request.query_params.get("project")
        else:
            # Retrieve the project URL the request data.
            project_url = request.data.get("project")

        # If a project URL is not provided, deny permission with a message.
        if not project_url:
            raise PermissionDenied("Project URL is required.")

        # Extract the project ID from the URL.
        project_id = self.extract_project_id(project_url)

        # Try to fetch the project with the given ID.
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise PermissionDenied("Project does not exist.")

        # Check if the user making the request is the author of the project.
        if project.author != request.user:
            raise PermissionDenied("You do not have to add contributors to this project.")

        return True

    def extract_project_id(self, url):
        # regular expression to extract the project ID from the URL.
        match = re.search(r'api/projects/(\d+)/$', url)
        if match:
            # Extract the project ID from the URL.
            return match.group(1)
        else:
            # If a valid ID is not found in the URL, raise an exception.
            raise PermissionDenied("Invalid project URL.")


class IsProjectAuthorForDelete(BasePermission):
    """
    Permission to allow only the author of a project to delete a contributor.
    """
    def has_permission(self, request, view):
        if request.method != "DELETE":
            return True

        project_id = request.query_params.get("project_id")
        if not project_id:
            raise PermissionDenied("Project ID is required.")

        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            raise PermissionDenied("Project does not exist.")
        if project.author != request.user:
            raise PermissionDenied("You do not have permission to delete contributors from this project.")

        return True

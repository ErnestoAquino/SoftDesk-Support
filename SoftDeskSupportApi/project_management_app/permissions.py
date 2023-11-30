from rest_framework.permissions import BasePermission

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



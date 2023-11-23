from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS
from rest_framework.exceptions import PermissionDenied


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

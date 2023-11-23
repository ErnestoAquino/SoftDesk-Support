from rest_framework.exceptions import APIException
from rest_framework import status


class CustomAPIException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = "You do not have permission to perform this action."
    default_code = "permission_denied"

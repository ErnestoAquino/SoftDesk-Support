from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from user_contrib_app.permissions import UserProfilePermission
from user_contrib_app.models import CustomUser
from user_contrib_app.models import Contributor
from user_contrib_app.serializers import CustomUserSerializer
from user_contrib_app.serializers import ContributorSerializer


class CustomUsersViewset(ModelViewSet):

    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_permissions(self):
        # Check if the current action is 'create'
        if self.action == 'create':
            # If it is 'create', set permissions so that any user can access to allow the creation of a new user
            permission_classes = [AllowAny]
        else:
            # If it's not 'create', restrict access to only authenticated users
            # and those who have the UserProfilePermission
            permission_classes = [IsAuthenticated, UserProfilePermission]
        # Returns a list of instances of the permission classes
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        # Validate data with the serializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check the minimum age.
        if serializer.validated_data['age'] < CustomUser.AGE_MINIMUM:
            return Response({"age": [f"The minimum age is {CustomUser.AGE_MINIMUM} years."]},
                            status=status.HTTP_400_BAD_REQUEST)

        # If everything is okay, save the instance
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED, headers = headers)


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_queryset(self):
        return Contributor.objects.all()

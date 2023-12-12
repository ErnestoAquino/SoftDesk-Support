from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from user_contrib_app.permissions import UserProfilePermission
from user_contrib_app.permissions import IsProjectContributor
from user_contrib_app.permissions import IsProjectAuthor
from user_contrib_app.models import CustomUser
from user_contrib_app.models import Contributor
from user_contrib_app.serializers import CustomUserSerializer
from user_contrib_app.serializers import ContributorSerializer
from project_management_app.models import Project


class CustomUsersViewset(ModelViewSet):
    serializer_class = CustomUserSerializer

    def get_queryset(self):
        # Filter users based on their preference to share data
        return CustomUser.objects.filter(can_data_be_shared=True)

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
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Allows a user to delete their own account.
        """
        try:
            # Retrieve the user object
            user = CustomUser.objects.get(pk=pk)

            # Delete the user. Permissions have already been checked.
            user.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            # Raise a 404 error if the user does not exist
            raise Http404("User not found")


class ContributorViewset(ModelViewSet):
    serializer_class = ContributorSerializer

    def get_permissions(self):
        permissions_classes = [IsAuthenticated, IsProjectContributor]

        if self.action in ["create", "destroy"]:
            permissions_classes.append(IsProjectAuthor)
        return [permission() for permission in permissions_classes]

    def get_queryset(self):
        project_pk = self.kwargs.get("project_pk")
        return Contributor.objects.filter(project_id=project_pk)

    def create(self, request, *args, **kwargs):
        # Extract the project ID from the URL
        project_pk = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_pk)

        # Create a new instance of Contributor with the provided data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new contributor, associating it with the project and the user.
        serializer.save(project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # Extract the project ID from the URL
        project_pk = self.kwargs.get("project_pk")

        username = request.data.get("username")

        # Get instances of Project and CustomUser
        project = get_object_or_404(Project, pk=project_pk)
        user = get_object_or_404(CustomUser, username=username)

        # Find and delete the contributor
        contributor = get_object_or_404(Contributor, user=user, project=project)
        contributor.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

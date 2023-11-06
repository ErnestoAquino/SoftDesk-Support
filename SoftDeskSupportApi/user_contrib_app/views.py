from rest_framework import status
# from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from user_contrib_app.models import CustomUser
from user_contrib_app.serializers import CustomUserSerializer


class CustomUsersViewset(ModelViewSet):

    serializer_class = CustomUserSerializer

    def get_queryset(self):
        return CustomUser.objects.all()

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

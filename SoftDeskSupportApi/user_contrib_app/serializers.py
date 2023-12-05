from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.serializers import HyperlinkedRelatedField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import CharField

from user_contrib_app.models import CustomUser
from user_contrib_app.models import Contributor
from project_management_app.models import Project


class CustomUserSerializer(ModelSerializer):
    """
    Serializer for the CustomUser model.

    This serializer handles the creation and updating of users. For creation, it ensures
    a password is provided, and for updates, it securely manages password updates along
    with other user fields.

    The password is treated as a write-only field for security and is made optional in updates to allow
    partial updates without modifying the password.
    """
    password = CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "age", "can_be_contacted", "can_data_be_shared"]

    def create(self, validated_data):
        """
        Creates a new user with the validated data.

        Ensures that a password is provided when creating a new user.
        Raises a ValidationError if not provided.
        """
        if 'password' not in validated_data:
            raise ValidationError({"password": "Password is required to create a user."})

        can_be_contacted = validated_data.get('can_be_contacted', False)
        can_data_be_shared = validated_data.get('can_data_be_shared', False)

        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            age=validated_data['age'],
            can_be_contacted=can_be_contacted,
            can_data_be_shared=can_data_be_shared
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Updates an existing user with the validated data.

        If a password is included in the validated data, updates the user's password.
        Updates other user fields as necessary.
        """
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        # Iterating over each field in the validated data.
        # This loop updates the user instance with the new values for each field provided in the request.
        for attr, value in validated_data.items():
            setattr(instance, attr, value)  # Set the attribute on the instance with the new value.

        instance.save()
        return instance


class ContributorSerializer(ModelSerializer):
    """
    Serializer for the Contributor model.

    This serializer is used for handling the relationships between users and projects.
    It allows the addition and removal of contributors to a project by managing the user-project association.

    The 'user' field is represented by the username of the CustomUser model, allowing for easy identification
    and association. The 'project' field is read-only, as the project association is managed through the endpoint URL.
    """

    user = SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    project = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = ["user", "project"]

from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import PrimaryKeyRelatedField
from rest_framework.serializers import ValidationError
from rest_framework.serializers import CharField

from user_contrib_app.models import CustomUser
from user_contrib_app.models import Contributor


class CustomUserSerializer(ModelSerializer):
    """
    Handles user creation and updates. Passwords are managed securely and required for new users.
    """
    password = CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "age", "can_be_contacted", "can_data_be_shared"]

    def create(self, validated_data):
        """
        Creates a new user, ensuring password provision.
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
        Updates user information, handling password changes securely.
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
    Manages contributors to projects, linking users with projects.
    """

    user = SlugRelatedField(slug_field="username", queryset=CustomUser.objects.all())
    project = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = ["user", "project"]

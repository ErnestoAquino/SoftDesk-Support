from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    AGE_MINIMUM = 15

    age = models.IntegerField()
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['age']


class Contributor(models.Model):
    user = models.ForeignKey(CustomUser,
                             on_delete=models.CASCADE,
                             related_name="contributions")
    project = models.ForeignKey("project_management_app.Project",
                                on_delete=models.CASCADE,
                                related_name="projects_contributors")

    class Meta:
        unique_together = ("user", "project")

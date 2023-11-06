from django.db import models
from user_contrib_app.models import CustomUser


class Project(models.Model):
    TYPE_CHOICES = (
        ("backend", "Back-end"),
        ("frontend", "Front-end"),
        ("ios", "iOS"),
        ("android", "Android"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name="Authored_projects")
    contributors = models.ManyToManyField(CustomUser,
                                          through="user_contrib_app.Contributor",
                                          related_name="projects")
    created_time = models.DateTimeField(auto_now_add=True)

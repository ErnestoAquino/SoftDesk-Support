import uuid

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

    def __str__(self):
        return self.name


class Issue(models.Model):
    STATUS_CHOICES = (
        ("to_do", "To do"),
        ("in_progress", "In progress"),
        ("finished", "Finished"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    TAG_CHOICES = (
        ("bug", "Bug"),
        ("feature", "Feature"),
        ("task", "Task")
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="to_do")
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, default="low")
    tag = models.CharField(max_length=50, choices=TAG_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="issues")
    assignee = models.ForeignKey(CustomUser,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="assigned_issues")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_issues")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="authored_comments")
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="issue_comments")
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.created_time}"

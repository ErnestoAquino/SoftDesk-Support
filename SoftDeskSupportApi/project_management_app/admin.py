from django.contrib import admin
from project_management_app.models import Project
from project_management_app.models import Issue
from project_management_app.models import Comment


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Columns to be displayed in the project listing.
    list_display = ('id', 'name', 'type', 'author', 'created_time')


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # Columns to be displayed in the issue listing.
    list_display = ('id', 'title', 'description', 'status', 'priority', 'tag', 'created_time')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # Columns to be displayed in the project listing.
    list_display = ('id', 'description', 'author', 'issue', 'created_time')

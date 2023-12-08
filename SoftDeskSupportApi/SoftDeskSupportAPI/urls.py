"""
URL configuration for SoftDeskSupportAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

from user_contrib_app.views import CustomUsersViewset
from user_contrib_app.views import ContributorViewset
from project_management_app.views import ProjectViewSet
from project_management_app.views import IssueViewSet
from project_management_app.views import CommentViewSet

router = routers.SimpleRouter()

router.register("users", CustomUsersViewset, basename="users")
router.register('contributors', ContributorViewset, basename="contributors")
router.register("projects", ProjectViewSet, basename="projects")
router.register("issues", IssueViewSet, basename="issues")
router.register("comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include('rest_framework.urls')),
    path("api/token/", TokenObtainPairView.as_view()),
    path("api/token/refresh/", TokenRefreshView.as_view()),
    path("api/", include(router.urls)),

    path("api/projects/<int:project_pk>/issues/",
         IssueViewSet.as_view({"get": "list", "post": "create"}),
         name="issue-list"),
    path("api/projects/<int:project_pk>/issues/<int:pk>/",
         IssueViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy", "patch": "partial_update"}),
         name="issue-detail"),

    path("api/projects/<int:project_pk>/contributors/",
         ContributorViewset.as_view({"get": "list", "post": "create", "delete": "destroy"})),

    path("api/projects/<int:project_pk>/issues/<int:issue_pk>/comments/",
         CommentViewSet.as_view({"get": "list", "post": "create"}),
         name="comment-list"),

    path("api/projects/<int:project_pk>/issues/<int:issue_pk>/comments/<uuid:pk>/",
         CommentViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy", "patch": "partial_update"}),
         name="comment-detail")
]

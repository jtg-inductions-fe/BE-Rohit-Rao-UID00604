from django.contrib import admin
from projects import models as projects_models


@admin.register(projects_models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "max_members", "status")
    list_filter = ("max_members", "status")


@admin.register(projects_models.ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "member")

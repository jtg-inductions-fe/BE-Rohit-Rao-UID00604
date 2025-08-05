from django.contrib import admin
from projects.models import Project, ProjectMember


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "max_members", "status")
    list_filter = ("max_members", "status")


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "member")

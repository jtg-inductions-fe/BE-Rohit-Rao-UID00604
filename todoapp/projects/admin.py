from django.contrib import admin
from projects.models import Project , ProjectMember

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "list_members", "max_members", "status")
    list_filter = ("max_members", "status")

    def list_members(self, obj):
        return ", ".join([str(user) for user in obj.members.all()])

    list_members.short_description = "Members"

@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ("project", "member")

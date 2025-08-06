from rest_framework import serializers

from projects import models as projects_models
from users.serializers import UserTodosStatsSerializer
from django.contrib.auth import get_user_model


class ProjectReportSerializer(serializers.Serializer):
    report = UserTodosStatsSerializer(many=True, source="members", exclude=["id"])
    project_title = serializers.CharField(source="name")

    class Meta:
        model = projects_models.Project
        fields = ["project_title", "report"]


class ProjectMemberSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False
    )

    def add_members(self, project):
        logs = {}
        user_ids = self.validated_data["user_ids"]
        current_count = projects_models.ProjectMember.objects.filter(
            project=project
        ).count()
        available_slots = project.max_members - current_count

        for user_id in user_ids:
            try:
                user = get_user_model().objects.get(id=user_id)
            except get_user_model().DoesNotExist:
                logs[user_id] = "User does not exist"
                continue

            if projects_models.ProjectMember.objects.filter(
                project=project, member=user
            ).exists():
                logs[user_id] = "User is already a Member"
                continue

            if projects_models.ProjectMember.objects.filter(member=user).count() >= 2:
                logs[user_id] = "Cannot add as User is a member in two projects"
                continue

            if available_slots <= 0:
                logs[user_id] = "Cannot add as Project already has maximum members"
                continue

            projects_models.ProjectMember.objects.create(member=user, project=project)
            logs[user_id] = "Member added Successfully"
            available_slots -= 1

        return logs

    def remove_members(self, project):
        logs = {}
        user_ids = self.validated_data["user_ids"]

        for user_id in user_ids:
            try:
                user = get_user_model().objects.get(id=user_id)
            except get_user_model().DoesNotExist:
                logs[user_id] = "User does not exist"
                continue

            membership = projects_models.ProjectMember.objects.filter(
                project=project, member=user
            )
            if not membership.exists():
                logs[user_id] = "User is not a member of this project"
                continue

            membership.delete()
            logs[user_id] = "User removed successfully"

        return logs

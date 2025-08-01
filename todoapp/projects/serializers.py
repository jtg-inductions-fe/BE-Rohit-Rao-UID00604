from rest_framework import serializers

from projects import models as projects_models
from users.serializers import UserTodosStatsSerializer


class ProjectReportSerializer(serializers.Serializer):
    report = UserTodosStatsSerializer(many=True, source="members", exclude=["id"])
    project_title = serializers.CharField(source="name")

    class Meta:
        model = projects_models.Project
        fields = ["project_title", "report"]

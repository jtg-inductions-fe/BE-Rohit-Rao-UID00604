from rest_framework import serializers

from projects.models import Project
from users.serializers import UserTodosStatsSerializer


class ProjectReportSerializer(serializers.Serializer):
    report = UserTodosStatsSerializer(many=True, source="members", exclude=["id"])
    project_title = serializers.CharField(source="name")

    class Meta:
        model = Project
        fields = ["project_title", "report"]

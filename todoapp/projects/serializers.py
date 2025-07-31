from rest_framework import serializers
from users.serializers import UserTodosStatsSerializer
from projects.models import Project


class ProjectReportSerializer(serializers.ModelSerializer):
    report = UserTodosStatsSerializer(many=True, source="members", exclude=["id"])
    project_title = serializers.CharField(source="name")

    class Meta:
        model = Project
        fields = ["project_title", "report"]
        # fields = "__all__"

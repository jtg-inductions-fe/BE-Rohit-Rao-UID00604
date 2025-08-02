from django.contrib.auth import get_user_model
from rest_framework import serializers

from todos import models as todos_models
from users import serializers as user_serializers


class TodoWithUserSerializer(serializers.ModelSerializer):
    creator = user_serializers.CustomUserSerializer(
        read_only=True, source="user", exclude=["id"]
    )
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = todos_models.Todo
        fields = ["id", "name", "status", "created_at", "creator"]

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_created_at(self, obj):
        return obj.date_created.strftime("%I:%M %p, %d %b, %Y")


class TodoSerializer(serializers.ModelSerializer):
    todo_id = serializers.IntegerField(source="id")
    todo = serializers.CharField(source="name")

    class Meta:
        model = todos_models.Todo
        fields = ["todo_id", "todo", "done"]


class TodoCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        source="user", queryset=get_user_model().objects.all(), write_only=True
    )
    todo = serializers.CharField(source="name")

    class Meta:
        model = todos_models.Todo
        fields = ["user_id", "todo", "done", "date_created"]

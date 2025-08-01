from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.serializers import CustomUserSerializer
from todos.models import Todo


class TodoWithUserSerializer(serializers.ModelSerializer):
    creator = CustomUserSerializer(read_only=True, source="user", exclude=["id"])
    status = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Todo
        fields = ["id", "name", "status", "created_at", "creator"]

    def get_status(self, obj):
        return "Done" if obj.done else "To Do"

    def get_created_at(self, obj):
        return obj.date_created.strftime("%I:%M %p, %d %b, %Y")

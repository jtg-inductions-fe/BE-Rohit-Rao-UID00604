from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        exclude = kwargs.pop("exclude", None)
        super().__init__(*args, **kwargs)

        if exclude is not None:

            not_allowed = set(exclude)
            existing = set(self.fields)

            for field_name in not_allowed & existing:
                self.fields.pop(field_name)

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "email"]


class UserTodosStatsSerializer(CustomUserSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta(CustomUserSerializer.Meta):
        model = CustomUser
        fields = CustomUserSerializer.Meta.fields + ["completed_count", "pending_count"]


class UserProjectStatsSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "to_do_projects",
            "in_progress_projects",
            "completed_projects",
        ]

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


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
        model = get_user_model()
        fields = ["id", "first_name", "last_name", "email"]


class UserTodosStatsSerializer(CustomUserSerializer):
    completed_count = serializers.IntegerField()
    pending_count = serializers.IntegerField()

    class Meta(CustomUserSerializer.Meta):
        model = get_user_model()
        fields = CustomUserSerializer.Meta.fields + ["completed_count", "pending_count"]


class UserProjectStatsSerializer(serializers.ModelSerializer):
    to_do_projects = serializers.ListField(child=serializers.CharField())
    in_progress_projects = serializers.ListField(child=serializers.CharField())
    completed_projects = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "to_do_projects",
            "in_progress_projects",
            "completed_projects",
        ]


class CustomUserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        attrs["user"] = user
        return attrs

    class Meta:
        model = get_user_model()
        fields = "__all__"



class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "email",
            "password",
            "date_joined",
            "confirm_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        token, _ = Token.objects.get_or_create(user=instance)
        data["token"] = token.key
        return data

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password and Confirm Password do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = get_user_model().objects.create_user(**validated_data)
        return user

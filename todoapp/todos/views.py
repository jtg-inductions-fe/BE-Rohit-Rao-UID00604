from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from todos import serializers as todos_serializers, models as todos_models


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class TodoAPIViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwner]
    """
        success response for create/update/get
        {
          "name": "",
          "done": true/false,
          "date_created": ""
        }

        success response for list
        [
          {
            "name": "",
            "done": true/false,
            "date_created": ""
          }
        ]
    """

    def get_serializer_class(self):
        if self.action == "create":
            return todos_serializers.TodoCreateSerializer

        return todos_serializers.TodoSerializer

    def create(self, request, *args, **kwargs):
        request.data["user_id"] = request.user.id
        return super().create(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == "list":
            user_id = self.request.user.id
            if user_id:
                return todos_models.Todo.objects.filter(user_id=user_id).order_by(
                    "-date_created"
                )
            return todos_models.Todo.objects.none()
        return todos_models.Todo.objects.all()

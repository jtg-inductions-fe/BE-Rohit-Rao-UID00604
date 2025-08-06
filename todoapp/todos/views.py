from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from todos import serializers as todos_serializers, models as todos_models


class TodoAPIViewSet(ModelViewSet):
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
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = todos_serializers.TodoCreateSerializer

        return todos_serializers.TodoSerializer

    def get_queryset(self):
        if self.action == "list":
            user_id = self.request.GET["user_id"]
            if user_id:
                return todos_models.Todo.objects.filter(user_id=user_id).order_by(
                    "-date_created"
                )
            return todos_models.Todo.objects.none()
        return todos_models.Todo.objects.all()

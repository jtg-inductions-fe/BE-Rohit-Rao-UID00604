from rest_framework.viewsets import ModelViewSet
from todos.models import Todo
from todos.serializers import TodoListSerializer, TodoSerializer
from rest_framework.permissions import AllowAny


class TodoAPIViewSet(ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

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
        if self.action == "list":
            self.serializer_class = TodoListSerializer

        print(self.action)
        return super().get_serializer_class()

  
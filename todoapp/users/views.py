from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.routers import Response

from django.contrib.auth import get_user_model
from users import serializers as users_serializers


class UserRegistrationAPIView(CreateAPIView):
    """
    success response format
     {
       first_name: "",
       last_name: "",
       email: "",
       date_joined: "",
       "token"
     }
    """

    serializer_class = users_serializers.UserRegistrationSerializer
    queryset = get_user_model()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "date_joined": user.date_joined,
                "token": token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class UserLoginAPIView(ObtainAuthToken):
    """
    success response format
      {
        auth_token: ""
      }
    """

    serializer_class = users_serializers.CustomUserLoginSerializer

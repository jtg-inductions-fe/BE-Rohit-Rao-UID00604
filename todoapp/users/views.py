from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView

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


class UserLoginAPIView(ObtainAuthToken):
    """
    success response format
      {
        auth_token: ""
      }
    """

    serializer_class = users_serializers.CustomUserLoginSerializer

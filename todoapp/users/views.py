from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

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
    permission_classes = [AllowAny]
    serializer_class = users_serializers.UserRegistrationSerializer


class UserLoginAPIView(ObtainAuthToken):
    """
    success response format
      {
        auth_token: ""
      }
    """
    permission_classes = [AllowAny]
    serializer_class = users_serializers.CustomUserLoginSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if "token" in response.data:
            response.data = {"auth_token": response.data["token"]}
        return response
from rest_framework import status
from rest_framework.generics import (
    UpdateAPIView,
    CreateAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
)
from .serializers import (
    ChangePasswordSerializer,
    RegisterSerializer,
)
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


# Change password view
class ChangePasswordView(UpdateAPIView):
    """
    Takes user old_password and new_password to change user password
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'message': 'Password updated successfully',
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Register View
class RegisterView(CreateAPIView):
    """
    Takes a set of user data and returns user information
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# Logout View
class LogoutView(APIView):
    """
    Takes user (refresh_token) to logout from this device
    or takes (all) to logout from all devices to this user
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        if 'refresh_token' not in self.request.data:
            return Response({"refresh_token": "Please enter refresh_token"}, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = self.request.data.get('refresh_token')
        try:
            token = RefreshToken(token=refresh_token)
            token.blacklist()
        except:
            return Response({"refresh_token": "Enter valid refresh_token"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "OK, goodbye"})


# Hello View
class HelloView(APIView):
    """
    Test view to return Hello
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return Response({"status": "Hello"}, status=status.HTTP_200_OK)

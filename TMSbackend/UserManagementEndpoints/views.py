from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from UserManagementEndpoints import serializer

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """Create a new standard user"""

    serializer_class = serializer.UserSerializer


class CreateManagerView(generics.CreateAPIView):
    """Create a new manager user"""

    serializer_class = serializer.ManagerSerializer

class AuthTokenView(ObtainAuthToken):
    """Create a new authentication token for user"""

    serializer_class = serializer.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage user data"""
    serializer_class = serializer.UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self):
        """Retreive and returns the user model"""

        return self.request.user
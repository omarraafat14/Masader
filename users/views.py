from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken , RefreshToken
from .serializers import UserSerializer


# Create your views here.
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if not username:
            return Response({'error': 'username is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password before saving
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer
    authentication_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(access), 'refresh': str(refresh)})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


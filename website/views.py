from rest_framework import generics

from .serializers import UserSerializer


class UserRegistration(generics.CreateAPIView):

    serializer_class = UserSerializer

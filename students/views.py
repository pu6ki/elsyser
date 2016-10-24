from django.contrib.auth.models import User

from rest_framework import generics
from rest_framework.response import Response

from .serializers import StudentSerializer


class StudentRegistration(generics.CreateAPIView):

    serializer_class = StudentSerializer


class StudentLogin(generics.CreateAPIView):

    serializer_class = StudentSerializer


class StudentProfile(generics.RetrieveAPIView):

    serializer_class = StudentSerializer

    def get(self, request, format=None):
        student = User.objects.get(username=request.user)
        serializer = StudentSerializer(student)

        return Response(serializer.data)

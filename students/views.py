from rest_framework import generics

from .serializers import StudentSerializer


class StudentRegistration(generics.CreateAPIView):

    serializer_class = StudentSerializer

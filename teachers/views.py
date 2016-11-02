from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .serializers import ExamSerializer


class AddExam(generics.CreateAPIView):

    permission_classes = (IsAdminUser,)
    serializer_class = ExamSerializer


class EditExam(generics.UpdateAPIView):

    permission_classes = (IsAdminUser,)
    serializer_class = ExamSerializer

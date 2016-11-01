from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from .serializers import (
    StudentSerializer,
    StudentProfileSerializer,
    ExamSerializer,
    NewsSerializer,
)
from .models import Student, Exam, News


class StudentRegistration(generics.CreateAPIView):

    serializer_class = StudentSerializer


class StudentProfile(generics.RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = StudentProfileSerializer

    def retrieve(self, request):
        student = Student.objects.get(user=request.user)
        serializer = StudentProfileSerializer(student)

        return Response(serializer.data)


class ExamsList(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ExamSerializer

    def get_queryset(self):
        return Exam.objects.filter(
            date__gte=datetime.now().date(),
            clazz=self.request.user.student.clazz,
        )


class NewsList(generics.ListAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = NewsSerializer

    def get_queryset(self):
        return News.objects.filter(clazz=self.request.user.student.clazz)

from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from datetime import datetime

from .serializers import (
    StudentSerializer,
    UserLoginSerializer,
    StudentProfileSerializer,
    ExamSerializer,
    NewsSerializer,
    HomeworkSerializer
)
from .models import Student, Exam, News, Homework


class StudentRegistration(generics.CreateAPIView):

    serializer_class = StudentSerializer


class UserLogin(generics.CreateAPIView):

    serializer_class = UserLoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({'token': token.key})


class StudentProfile(generics.RetrieveAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentProfileSerializer


    def get(self, request, format=None):
        student = Student.objects.get(user=request.user)
        serializer = self.serializer_class(student)

        return Response(serializer.data)


class ExamsList(generics.ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ExamSerializer


    def get_queryset(self):
        return Exam.objects.filter(
            date__gte=datetime.now().date(),
            clazz=self.request.user.student.clazz,
        )


class NewsViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = NewsSerializer


    def get_queryset(self):
        return News.objects.filter(
            author__student__clazz=self.request.user.student.clazz
        )


    def retrieve(self, request, pk=None):
        news = get_object_or_404(
            News.objects.filter(
                author__student__clazz=self.request.user.student.clazz
            ), id=pk
        )
        serializer = self.serializer_class(news)

        return Response(serializer.data)


    def create(self, request):
        news = News.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            author=request.user
        )
        serializer = self.serializer_class(news)

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class HomeworksList(generics.ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = HomeworkSerializer


    def get_queryset(self):
        return Homework.objects.filter(
            deadline__gte=datetime.now().date(),
            clazz=self.request.user.student.clazz
        )

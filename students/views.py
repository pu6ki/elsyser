from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import detail_route
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
    HomeworkSerializer,
    CommentSerializer
)
from .models import Student, Exam, News, Homework, Comment


class StudentRegistration(generics.CreateAPIView):

    serializer_class = StudentSerializer


class UserLogin(generics.CreateAPIView):

    serializer_class = UserLoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        request.session.set_expiry(1209600)

        return Response({'token': token.key})


class StudentProfile(generics.RetrieveUpdateAPIView):

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


    def retrieve(self, request, pk=None):
        news = get_object_or_404(
            News.objects.filter(
                author__clazz=self.request.user.student.clazz
            ), id=pk
        )
        serializer = self.serializer_class(news)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk=None):
        news = get_object_or_404(News, id=pk)

        if news.author != request.user.student:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        news.__dict__.update(**request.data.dict())
        news.save()

        serializer = self.serializer_class(news)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        return News.objects.filter(
            author__clazz=self.request.user.student.clazz
        )


    def create(self, request):
        context = {'request': request}
        serializer = self.serializer_class(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )


    @detail_route(methods=['post'])
    def add_comment(self, request, pk=None):
        news = get_object_or_404(News, id=pk)
        context = {'request': request, 'news': news}

        serializer = CommentSerializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )


class HomeworksList(generics.ListAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = HomeworkSerializer


    def get_queryset(self):
        return Homework.objects.filter(
            deadline__gte=datetime.now().date(),
            clazz=self.request.user.student.clazz
        )

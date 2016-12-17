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
    StudentSerializer, UserLoginSerializer, StudentProfileSerializer,
    ExamSerializer,
    NewsSerializer, CommentSerializer,
    HomeworkSerializer,
)
from .models import Student, Exam, News, Homework, Comment
from .permissions import IsStudent, IsTeacher


class StudentRegistration(generics.CreateAPIView):

    serializer_class = StudentSerializer


class UserLogin(generics.CreateAPIView):

    serializer_class = UserLoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        is_teacher = user.groups.filter(name='Teachers').exists()

        return Response({'token': token.key, 'is_teacher': is_teacher})


class StudentProfile(generics.RetrieveUpdateAPIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = StudentProfileSerializer


    def get(self, request, format=None):
        student = Student.objects.get(user=request.user)
        serializer = self.serializer_class(student)

        return Response(serializer.data)


    def update(self, request, format=None):
        student = Student.objects.get(user=request.user)

        serializer = self.serializer_class(
            student, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ExamsViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = ExamSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated, IsTeacher],
        'update': [IsAuthenticated, IsTeacher],
        'destroy': [IsAuthenticated, IsTeacher],
        'list': [IsAuthenticated, IsStudent],
        'retrieve': [IsAuthenticated, IsStudent],
    }


    def retrieve(self, request, pk=None):
        exam = get_object_or_404(
            Exam.objects.filter(clazz=request.user.student.clazz),
            id=pk
        )
        serializer = self.serializer_class(exam)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        return Exam.objects.filter(
            date__gte=datetime.now().date(),
            clazz=self.request.user.student.clazz,
        )


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )


    def update(self, request, pk=None):
        exam = get_object_or_404(Exam, id=pk)

        serializer = self.serializer_class(
            exam, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        exam = get_object_or_404(Exam, id=pk)
        exam.delete()

        return Response(
            {'message': 'Exam successfully deleted.'},
            status=status.HTTP_200_OK
        )


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]


class NewsViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = NewsSerializer


    def retrieve(self, request, pk=None):
        news = get_object_or_404(
            News.objects.filter(author__clazz=self.request.user.student.clazz),
            id=pk
        )
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


    def update(self, request, pk=None):
        news = get_object_or_404(News, id=pk)

        if news.author != request.user.student:
            return Response(
                {'message': 'You can edit only your own posts.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(
            news, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        news = get_object_or_404(News, id=pk)

        if news.author != request.user.student:
            return Response(
                {'message': 'You can delete only your own posts.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        news.delete()

        return Response(
            {'message': 'Post successfully deleted.'},
            status=status.HTTP_200_OK
        )


class CommentsViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsStudent)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


    def create(self, request, news_pk=None):
        news = get_object_or_404(News, id=news_pk)
        context = {'request': request, 'news': news}

        serializer = self.serializer_class(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )


    def update(self, request, news_pk=None, pk=None):
        news = get_object_or_404(News, id=news_pk)
        comment = get_object_or_404(news.comment_set, id=pk)

        if comment.posted_by != request.user.student:
            return Response(
                {'message': 'You can edit only your own comments.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.serializer_class(
            comment, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


    def destroy(self, request, news_pk=None, pk=None):
        news = get_object_or_404(News, id=news_pk)
        comment = get_object_or_404(news.comment_set, id=pk)

        if comment.posted_by != request.user.student:
            return Response(
                {'message': 'You can delete only your own comments.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        comment.delete()

        return Response(
            {'message': 'Comment successfully deleted.'},
            status=status.HTTP_200_OK
        )


class HomeworksViewSet(viewsets.ModelViewSet):

    authentication_classes = (TokenAuthentication,)
    serializer_class = HomeworkSerializer
    permission_classes_by_action = {
        'create': [IsAuthenticated, IsTeacher],
        'update': [IsAuthenticated, IsTeacher],
        'destroy': [IsAuthenticated, IsTeacher],
        'list': [IsAuthenticated, IsStudent],
        'retrieve': [IsAuthenticated, IsStudent],
    }


    def retrieve(self, request, pk=None):
        homework = get_object_or_404(
            Homework.objects.filter(clazz=request.user.student.clazz),
            id=pk
        )
        serializer = self.serializer_class(homework)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_queryset(self):
        return Homework.objects.filter(
            deadline__gte=datetime.now().date(),
            clazz=self.request.user.student.clazz
        )


    def create(self, request):
        context = {'request': request}

        serializer = self.serializer_class(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            serializer.validated_data, status=status.HTTP_201_CREATED
        )


    def update(self, request, pk=None):
        homework = get_object_or_404(Homework, id=pk)

        serializer = self.serializer_class(
            homework, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        homework = get_object_or_404(Homework, id=pk)
        homework.delete()

        return Response(
            {'message': 'Homework successfully deleted.'},
            status=status.HTTP_200_OK
        )


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

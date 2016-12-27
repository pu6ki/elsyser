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
    UserLoginSerializer, UserInfoSerializer,
    StudentSerializer, StudentProfileSerializer,
    ExamSerializer, ExamReadSerializer,
    NewsSerializer, CommentSerializer,
    HomeworkSerializer, HomeworkReadSerializer
)
from .models import Student, Exam, News, Homework, Comment, Subject, Class
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


class UserProfile(generics.RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_user_entry(self, request):
        user = request.user

        try:
            entry = Student.objects.get(user=user)
        except:
            entry = user

        return entry


    def get_serializer_class(self):
        return StudentProfileSerializer if Student.objects.filter(user=self.request.user).exists() else UserInfoSerializer


    def get(self, request, format=None):
        entry = self.get_user_entry(request)

        serializer = self.get_serializer(entry)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, format=None):
        entry = self.get_user_entry(request)

        serializer = self.get_serializer(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ExamsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated, IsTeacher],
        'update': [IsAuthenticated, IsTeacher],
        'destroy': [IsAuthenticated, IsTeacher],
    }


    def get_serializer_class(self):
        return ExamReadSerializer if self.request.method in ('GET',) else ExamSerializer


    def get_queryset(self):
        exams = Exam.objects.filter(date__gte=datetime.now())
        student = Student.objects.filter(user=self.request.user).first()

        return exams if not student else exams.filter(clazz=student.clazz)


    def retrieve(self, request, pk=None):
        exam = get_object_or_404(self.get_queryset(), id=pk)

        serializer = self.get_serializer(exam)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def create(self, request):
        context = {'request': request}

        subject = get_object_or_404(Subject, **request.data.get('subject'))
        clazz = get_object_or_404(Class, **request.data.get('clazz'))

        serializer = self.get_serializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(clazz=clazz, subject=subject)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


    def update(self, request, pk=None):
        exam = get_object_or_404(Exam, id=pk)

        if exam.author != request.user:
            return Response(
                {'message': 'You can edit only your own exams.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(
            exam, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def destroy(self, request, pk=None):
        exam = get_object_or_404(Exam, id=pk)

        if exam.author != request.user:
            return Response(
                {'message': 'You can delete only your own exams.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

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
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def get_queryset(self):
        return News.objects.filter(
            author__clazz=self.request.user.student.clazz
        )


    def create(self, request):
        context = {'request': request}

        serializer = self.serializer_class(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
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
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


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
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
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
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


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
    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated, IsTeacher],
        'update': [IsAuthenticated, IsTeacher],
        'destroy': [IsAuthenticated, IsTeacher],
    }


    def get_serializer_class(self):
        return HomeworkReadSerializer if self.request.method in ('GET',) else HomeworkSerializer


    def get_queryset(self):
        homeworks = Homework.objects.filter(deadline__gte=datetime.now())
        student = Student.objects.filter(user=self.request.user).first()

        return homeworks if not student else homeworks.filter(clazz=student.clazz)


    def retrieve(self, request, pk=None):
        homework = get_object_or_404(self.get_queryset(), id=pk)

        serializer = self.get_serializer(homework)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def create(self, request):
        context = {'request': request}

        subject = get_object_or_404(Subject, **request.data.get('subject'))
        clazz = get_object_or_404(Class, **request.data.get('clazz'))

        serializer = self.get_serializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(clazz=clazz, subject=subject)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


    def update(self, request, pk=None):
        homework = get_object_or_404(Homework, id=pk)

        if homework.author != request.user:
            return Response(
                {'message': 'You can edit only your own homeworks.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(
            homework, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def destroy(self, request, pk=None):
        homework = get_object_or_404(Homework, id=pk)

        if homework.author != request.user:
            return Response(
                {'message': 'You can delete only your own homeworks.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        homework.delete()

        return Response(
            {'message': 'Homework successfully deleted.'},
            status=status.HTTP_200_OK
        )


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

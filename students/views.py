from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import detail_route, list_route

from datetime import datetime

from .serializers import (
    UserLoginSerializer, UserInfoSerializer,
    StudentSerializer, StudentProfileSerializer,
    SubjectSerializer,
    ExamSerializer, ExamReadSerializer,
    NewsSerializer, CommentSerializer,
    HomeworkSerializer, HomeworkReadSerializer,
    MaterialSerializer
)
from .models import (
    Student, Exam, News, Homework, Comment, Subject, Class, Material
)
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
        return request.user if IsTeacher().has_permission(request, self) else request.user.student


    def get_serializer_class(self):
        return UserInfoSerializer if IsTeacher().has_permission(self.request, self) else StudentProfileSerializer


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


class SubjectsList(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = SubjectSerializer


    def get(self, request):
        serializer = self.serializer_class(Subject.objects.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
        request = self.request
        exams = Exam.objects.filter(date__gte=datetime.now())

        return exams if IsTeacher().has_permission(request, self) else exams.filter(clazz=request.user.student.clazz)


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


    def get_queryset(self):
        return News.objects.filter(
            author__clazz=self.request.user.student.clazz
        )


    def retrieve(self, request, pk=None):
        news = get_object_or_404(elf.get_queryset(), id=pk)
        serializer = self.serializer_class(news)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
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
        request = self.request
        homeworks = Homework.objects.filter(deadline__gte=datetime.now())

        return homeworks if IsTeacher().has_permission(request, self) else homeworks.filter(clazz=request.user.student.clazz)


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


class MaterialsViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': [IsAuthenticated],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated, IsTeacher],
    }
    serializer_class = MaterialSerializer


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]


class MaterialsListViewSet(mixins.ListModelMixin, MaterialsViewSet):
    def get_queryset(self):
        request = self.request
        all_materials = Material.objects.all()

        if IsTeacher().has_permission(request, self):
            return all_materials

        return all_materials.filter(class_number=request.user.student.clazz.number)


class MaterialsNestedViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, MaterialsListViewSet):
    def get_queryset(self):
        subject_id = self.kwargs['subject_pk']
        subject = get_object_or_404(Subject, id=subject_id)

        return super().get_queryset().filter(subject=subject)


    def retrieve(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        serializer = self.serializer_class(material)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, subject_pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        context = {'subject': subject}

        serializer = self.serializer_class(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

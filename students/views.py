from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import generics, viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from datetime import datetime

from students.serializers import (
    UserLoginSerializer, UserInfoSerializer,
    StudentSerializer,
    SubjectSerializer,
    StudentProfileSerializer, TeacherProfileSerializer,
    ExamSerializer, ExamReadSerializer,
    NewsSerializer,
    CommentSerializer, CommentReadSerializer,
    HomeworkSerializer, HomeworkReadSerializer,
    MaterialSerializer, MaterialReadSerializer,
    SubmissionSerializer, SubmissionReadSerializer
)
from students.models import (
    Student, Exam, News, Homework,
    Comment, Subject, Class, Material,
    Submission, Teacher
)
from students.permissions import IsStudent, IsTeacher


class StudentRegistration(generics.CreateAPIView):
    serializer_class = StudentSerializer


class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer


    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        response_data = UserInfoSerializer(user).data
        response_data['token'] = token.key
        response_data['is_teacher'] = Teacher.objects.filter(user=user).exists()

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


class ProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_entry_model(self, user):
        return Teacher.objects.filter(user=user).first() or Student.objects.filter(user=user).first()


    def get_serializer_model(self, user):
        return TeacherProfileSerializer if Teacher.objects.filter(user=user).exists() else StudentProfileSerializer


    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, id=pk)
        entry = self.get_entry_model(user)

        serializer = self.get_serializer_model(user)(entry)

        response_data = serializer.data
        response_data['can_edit'] = (user == request.user)

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


    def update(self, request, pk=None):
        user = get_object_or_404(User, id=pk)

        if user != request.user:
            return Response(
                {'message': 'You can only update your own profile.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        entry = self.get_entry_model(user)

        serializer = self.get_serializer_model(user)(
            entry, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK
        )


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
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher),
        'destroy': (IsAuthenticated, IsTeacher)
    }


    def get_serializer_class(self):
        return ExamReadSerializer if self.request.method in ('GET',) else ExamSerializer


    def get_queryset(self):
        request = self.request
        upcoming_exams = Exam.objects.filter(date__gte=datetime.now())

        if IsTeacher().has_permission(request, self):
            return upcoming_exams.filter(subject=request.user.teacher.subject)

        return upcoming_exams.filter(clazz=request.user.student.clazz)


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

        clazz = get_object_or_404(Class, **request.data.get('clazz'))

        serializer = self.get_serializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(clazz=clazz)
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
        news = get_object_or_404(self.get_queryset(), id=pk)
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
    queryset = Comment.objects.all()


    def get_serializer_class(self):
        return CommentReadSerializer if self.request.method in ('GET',) else CommentSerializer


    def create(self, request, news_pk=None):
        news = get_object_or_404(News, id=news_pk)
        context = {'request': request, 'news': news}

        serializer = self.get_serializer_class()(
            context=context, data=request.data
        )
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

        serializer = self.get_serializer_class()(
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
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher),
        'destroy': (IsAuthenticated, IsTeacher)
    }


    def get_serializer_class(self):
        return HomeworkReadSerializer if self.request.method in ('GET',) else HomeworkSerializer


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]


    def get_queryset(self):
        request = self.request
        upcoming_homeworks = Homework.objects.filter(deadline__gte=datetime.now())

        if IsTeacher().has_permission(request, self):
            return upcoming_homeworks.filter(subject=request.user.teacher.subject)

        return upcoming_homeworks.filter(clazz=request.user.student.clazz)


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

        clazz = get_object_or_404(Class, **request.data.get('clazz'))

        serializer = self.get_serializer(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(clazz=clazz)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


    def update(self, request, pk=None):
        homework = get_object_or_404(Homework, id=pk)

        if homework.author != request.user.teacher:
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

        if homework.author != request.user.teacher:
            return Response(
                {'message': 'You can delete only your own homeworks.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        homework.delete()

        return Response(
            {'message': 'Homework successfully deleted.'},
            status=status.HTTP_200_OK
        )


class MaterialsViewSet(viewsets.GenericViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher),
        'destroy': (IsAuthenticated, IsTeacher)
    }


    def get_serializer_class(self):
         return MaterialReadSerializer if self.request.method in ('GET',) else MaterialSerializer


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]


class MaterialsListViewSet(mixins.ListModelMixin, MaterialsViewSet):
    def get_queryset(self):
        request = self.request
        all_materials = Material.objects.all()

        if IsTeacher().has_permission(request, self):
            return all_materials.filter(subject=request.user.teacher.subject)

        return all_materials.filter(class_number=request.user.student.clazz.number)


class NestedMaterialsViewSet(mixins.RetrieveModelMixin,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             MaterialsListViewSet):

    def get_queryset(self):
        subject_id = self.kwargs['subject_pk']
        subject = get_object_or_404(Subject, id=subject_id)

        return super().get_queryset().filter(subject=subject)


    def retrieve(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        serializer = self.get_serializer(material)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, subject_pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        context = {'subject': subject, 'request': request}

        serializer = self.get_serializer_class()(
            context=context, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


    def update(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        if material.author != request.user:
            return Response(
                {'message': 'You can edit only your own materials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer_class()(
            material, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def destroy(self, request, subject_pk=None, pk=None):
        subject = get_object_or_404(Subject, id=subject_pk)
        material = get_object_or_404(subject.material_set, id=pk)

        if material.author != request.user:
            return Response(
                {'message': 'You can delete only your own materials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        material.delete()

        return Response(
            {'message': 'Material successfully deleted.'},
            status=status.HTTP_200_OK
        )


class SubmissionsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsStudent),
        'update': (IsAuthenticated, IsStudent),
        'destroy': (IsAuthenticated, IsStudent)
    }


    def get_queryset(self):
        request = self.request
        all_submissions = Submission.objects.all()

        if IsTeacher().has_permission(request, self):
            return all_submissions.filter(homework__subject=request.user.teacher.subject)

        return all_submissions.filter(student=request.user.student)


    def get_serializer_class(self):
         return SubmissionReadSerializer if self.request.method in ('GET',) else SubmissionSerializer


    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]


    def retrieve(self, request, homeworks_pk=None, pk=None):
        homework = get_object_or_404(Homework, id=homeworks_pk)
        submission = get_object_or_404(homework.submission_set, id=pk)

        serializer = self.get_serializer(submission)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def create(self, request, homeworks_pk=None):
        homework = get_object_or_404(Homework, id=homeworks_pk)
        context = {'request': request, 'homework': homework}

        serializer = self.get_serializer_class()(
            context=context, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


    def update(self, request, homeworks_pk=None, pk=None):
        homework = get_object_or_404(Homework, id=homeworks_pk)
        submission = get_object_or_404(homework.submission_set, id=pk)

        if submission.student != request.user.student:
            return Response(
                {'message': 'You can edit only your own submissions.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer_class()(
            submission, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.validated_data,
            status=status.HTTP_200_OK,
            headers=headers
        )


    def destroy(self, request, homeworks_pk=None, pk=None):
        homework = get_object_or_404(Homework, id=homeworks_pk)
        submission = get_object_or_404(homework.submission_set, id=pk)

        if submission.student != request.user.student:
            return Response(
                {'message': 'You can delete only your own submissions.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        submission.delete()

        return Response(
            {'message': 'Submission successfully deleted.'},
            status=status.HTTP_200_OK
        )

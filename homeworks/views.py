from datetime import datetime

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from students.models import Class
from students.permissions import IsStudent, IsTeacher, IsTeacherAuthor
from .serializers import (
    HomeworkSerializer, HomeworkReadSerializer, SubmissionSerializer, SubmissionReadSerializer
)
from .models import Homework, Submission
from .permissions import HasOnlyOneSubmission, IsValidStudent, IsNotChecked


class HomeworksViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsTeacherAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsTeacherAuthor)
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        return HomeworkReadSerializer if self.request.method in ('GET',) else HomeworkSerializer

    def get_queryset(self):
        request = self.request
        upcoming_homeworks = Homework.objects.filter(deadline__gte=datetime.now())

        if IsTeacher().has_permission(request, self):
            return upcoming_homeworks.filter(subject=request.user.teacher.subject)

        return upcoming_homeworks.filter(clazz=request.user.student.clazz)

    def retrieve(self, request, *args, **kwargs):
        homework = get_object_or_404(self.get_queryset(), id=kwargs['pk'])

        serializer = self.get_serializer(homework)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request, *args, **kwargs):
        clazz_data = request.data.get('clazz')
        clazz, _ = Class.objects.get_or_create(
            number=int(clazz_data['number']),
            letter=clazz_data['letter']
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(clazz=clazz)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        homework = get_object_or_404(Homework, id=kwargs['pk'])
        self.check_object_permissions(request, homework)

        serializer = self.get_serializer(homework, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        homework = get_object_or_404(Homework, id=kwargs['pk'])
        self.check_object_permissions(request, homework)

        homework.delete()

        return Response(
            {'message': 'Homework successfully deleted.'},
            status=status.HTTP_200_OK
        )


class SubmissionsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsValidStudent),
        'create': (IsAuthenticated, IsStudent, HasOnlyOneSubmission),
        'update': (IsAuthenticated, IsValidStudent, IsNotChecked),
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        is_get_request = self.request.method in ('GET',)

        return SubmissionReadSerializer if is_get_request else SubmissionSerializer

    def get_queryset(self):
        request = self.request

        homework = get_object_or_404(Homework, id=self.kwargs['homeworks_pk'])
        submissions = Submission.objects.filter(homework=homework)

        if IsStudent().has_permission(request, self):
            return submissions.filter(student=request.user.student)

        return submissions.filter(checked=False)

    def retrieve(self, request, *args, **kwargs):
        homework = get_object_or_404(Homework, id=kwargs['homeworks_pk'])
        submission = get_object_or_404(homework.submission_set, id=kwargs['pk'])

        if IsStudent().has_permission(request, self):
            self.check_object_permissions(request, submission)

        serializer = self.get_serializer(submission)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def create(self, request, *args, **kwargs):
        homework = get_object_or_404(Homework, id=kwargs['homeworks_pk'])
        self.check_object_permissions(request, homework)

        context = {'request': request, 'homework': homework}

        serializer = self.get_serializer_class()(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        homework = get_object_or_404(Homework, id=kwargs['homeworks_pk'])
        submission = get_object_or_404(homework.submission_set, id=kwargs['pk'])

        if IsStudent().has_permission(request, self):
            self.check_object_permissions(request, submission)

        serializer = self.get_serializer(submission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

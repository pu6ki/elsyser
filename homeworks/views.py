from datetime import datetime
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from homeworks.serializers import (
    HomeworkSerializer, HomeworkReadSerializer,
    SubmissionSerializer, SubmissionReadSerializer
)
from homeworks.models import Homework, Submission

from students.models import Class
from students.permissions import IsStudent, IsTeacher


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
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

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

        clazz_data = request.data.get('clazz')
        clazz, _ = Class.objects.get_or_create(
            number=int(clazz_data['number']),
            letter=clazz_data['letter']
        )

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


class SubmissionsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsStudent),
        'update': (IsAuthenticated,),
    }


    def get_queryset(self):
        request = self.request

        homework = get_object_or_404(Homework, id=self.kwargs['homeworks_pk'])
        submissions = Submission.objects.filter(homework=homework)

        if IsStudent().has_permission(request, self):
            return submissions.filter(student=request.user.student)

        return submissions.filter(checked=False)

    def get_serializer_class(self):
         return SubmissionReadSerializer if self.request.method in ('GET',) else SubmissionSerializer

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_classes_by_action[
                self.action
            ]
        ]

    def retrieve(self, request, homeworks_pk=None, pk=None):
        homework = get_object_or_404(Homework, id=homeworks_pk)
        submission = get_object_or_404(homework.submission_set, id=pk)

        if IsStudent().has_permission(request, self):
            if submission.student != request.user.student:
                return Response(
                    {'message': 'You can view only your own submissions.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        serializer = self.get_serializer(submission)
        headers = self.get_success_headers(serializer.data)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers=headers
        )

    def create(self, request, homeworks_pk=None):
        homework = get_object_or_404(Homework, id=homeworks_pk)

        if homework.submission_set.filter(student=request.user.student):
            return Response(
                {'message': 'You can add only one submission.'},
                status=status.HTTP_403_FORBIDDEN
            )

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

        if IsStudent().has_permission(request, self):
            if submission.student != request.user.student or submission.checked:
                return Response(
                    {'message': 'You can not perform this action.'},
                    status=status.HTTP_403_FORBIDDEN
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

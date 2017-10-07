from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_word_filter import FullWordSearchFilter

from students.models import Class
from students.permissions import IsStudent, IsTeacher, IsTeacherAuthor

from .serializers import (
    HomeworkSerializer, HomeworkReadSerializer, SubmissionSerializer, SubmissionReadSerializer
)
from .models import Homework
from .permissions import HasOnlyOneSubmission, IsValidStudent, IsNotChecked
from .filters import HomeworksFilterBackend, SubmissionsFilterBackend


class HomeworksViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsTeacherAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsTeacherAuthor)
    }
    queryset = Homework.objects.filter(deadline__gte=datetime.now())
    filter_backends = (HomeworksFilterBackend, FullWordSearchFilter)
    word_fields = ('topic', 'subject__title', 'author__user__username')

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        return HomeworkReadSerializer if self.request.method in ('GET',) else HomeworkSerializer

    def create(self, request, *args, **kwargs):
        clazz_data = request.data.get('clazz', {})
        clazz = get_object_or_404(Class, **clazz_data)
        context = {'request': request, 'clazz': clazz}

        serializer = self.get_serializer_class()(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class SubmissionsViewSet(viewsets.ModelViewSet):
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated, IsValidStudent),
        'create': (IsAuthenticated, IsStudent, HasOnlyOneSubmission),
        'update': (IsAuthenticated, IsValidStudent, IsNotChecked),
    }
    filter_backends = (SubmissionsFilterBackend, FullWordSearchFilter)
    word_fields = ('student__user__username',)
    pagination_class = None

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        return SubmissionReadSerializer if self.request.method in ('GET',) else SubmissionSerializer

    def get_related_homework(self):
        return get_object_or_404(Homework, id=self.kwargs['homeworks_pk'])

    def get_queryset(self):
        homework = self.get_related_homework()

        return homework.submissions

    def get_object(self):
        return get_object_or_404(self.get_queryset(), id=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        submission = self.get_object()

        if IsStudent().has_permission(request, self):
            self.check_object_permissions(request, submission)

        serializer = self.get_serializer(submission)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def create(self, request, *args, **kwargs):
        homework = self.get_related_homework()
        self.check_object_permissions(request, homework)

        context = {'request': request, 'homework': homework}

        serializer = self.get_serializer_class()(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        submission = self.get_object()

        if IsStudent().has_permission(request, self):
            self.check_object_permissions(request, submission)

        serializer = self.get_serializer(submission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_200_OK, headers=headers)

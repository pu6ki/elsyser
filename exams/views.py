from datetime import datetime
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import ExamSerializer, ExamReadSerializer
from .models import Exam
from students.models import Class
from students.permissions import IsTeacher, IsTeacherAuthor


class ExamsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsTeacherAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsTeacherAuthor)
    }

    def get_serializer_class(self):
        return ExamReadSerializer if self.request.method in ('GET',) else ExamSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

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

        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

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
        exam = get_object_or_404(Exam, id=pk)
        self.check_object_permissions(request, exam)

        serializer = self.get_serializer(exam, data=request.data, partial=True)
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
        self.check_object_permissions(request, exam)

        exam.delete()

        return Response(
            {'message': 'Exam successfully deleted.'},
            status=status.HTTP_200_OK
        )

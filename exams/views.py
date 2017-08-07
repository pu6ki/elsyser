from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework_word_filter import FullWordSearchFilter

from students.permissions import IsTeacher, IsTeacherAuthor

from .serializers import ExamSerializer, ExamReadSerializer
from .models import Exam
from .filters import ExamsFilterBackend


class ExamsViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes_by_action = {
        'list': (IsAuthenticated,),
        'retrieve': (IsAuthenticated,),
        'create': (IsAuthenticated, IsTeacher),
        'update': (IsAuthenticated, IsTeacher, IsTeacherAuthor),
        'destroy': (IsAuthenticated, IsTeacher, IsTeacherAuthor)
    }
    queryset = Exam.objects.filter(date__gte=datetime.now())
    filter_backends = (ExamsFilterBackend, FullWordSearchFilter)
    word_fields = ('topic',)

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_serializer_class(self):
        return ExamReadSerializer if self.request.method in ('GET',) else ExamSerializer

    def create(self, request, *args, **kwargs):
        context = {'request': request}

        serializer = self.get_serializer_class()(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        exam = get_object_or_404(Exam, id=kwargs['pk'])
        self.check_object_permissions(request, exam)

        serializer = self.get_serializer(exam, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

from django.contrib.auth import login

from collections import defaultdict

from django.contrib.auth.models import User

from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework_word_filter import FullWordSearchFilter

from .serializers import (
    UserLoginSerializer, UserInfoSerializer,
    ClassSerializer,
    StudentSerializer,
    SubjectSerializer,
    StudentProfileSerializer, TeacherProfileSerializer,
    GradesSerializer
)
from .models import Subject, Class, Student, Teacher, Grade
from .permissions import IsValidUser, IsStudent, IsTeacher, IsTeachersSubject
from .filters import GradeFilterBackend


class StudentRegistration(generics.CreateAPIView):
    serializer_class = StudentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        user_email = serializer.validated_data['user']['email']
        response = {
            'message': 'Verification email has been sent to {email}.'.format(email=user_email)
        }

        return Response(response, status=status.HTTP_201_CREATED, headers=headers)


class AccountActivation(generics.UpdateAPIView):
    serializer_class = UserInfoSerializer

    def update(self, request, *args, **kwargs):
        user = generics.get_object_or_404(User, student__activation_key=kwargs['activation_key'])
        user.is_active = True
        user.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class UserLogin(generics.CreateAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        login(request, user)

        response_data = UserInfoSerializer(user).data
        response_data['token'] = token.key
        response_data['is_teacher'] = Teacher.objects.filter(user=user).exists()

        headers = self.get_success_headers(serializer.data)

        return Response(response_data, status=status.HTTP_200_OK, headers=headers)


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    permission_classes_by_action = {
        'retrieve': (IsAuthenticated,),
        'update': (IsAuthenticated, IsValidUser),
    }

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.action]
        ]

    def get_entry_model(self, user):
        teachers = Teacher.objects.filter(user=user)
        students = Student.objects.filter(user=user)

        return teachers.first() or students.first()

    def get_serializer_model(self, user):
        teachers = Teacher.objects.filter(user=user)

        return TeacherProfileSerializer if teachers else StudentProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        user = generics.get_object_or_404(User, id=kwargs['pk'])
        entry = self.get_entry_model(user)

        serializer = self.get_serializer_model(user)(entry)

        response_data = serializer.data
        response_data['can_edit'] = (user == request.user)

        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        user = generics.get_object_or_404(User, id=kwargs['pk'])
        self.check_object_permissions(request, user)

        entry = self.get_entry_model(user)

        serializer = self.get_serializer_model(user)(entry, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class SubjectsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


class ClassesList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ClassSerializer

    def get_queryset(self):
        all_classes = Class.objects.all()
        class_number = self.request.query_params.get('number')

        return all_classes.filter(number=class_number) if class_number else all_classes

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)

        data = defaultdict(list)
        for clazz in serializer.data:
            data[clazz['number']].append(clazz)

        return Response(data, status=status.HTTP_200_OK)


class StudentsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentProfileSerializer
    queryset = Student.objects.all()
    filter_backends = (FullWordSearchFilter,)
    word_fields = ('user__username',)

    def get_queryset(self):
        all_students = Student.objects.all()
        class_number = self.request.query_params.get('class_number')
        class_letter = self.request.query_params.get('class_letter', '')

        students_by_number = all_students.filter(clazz__number=class_number)
        students_by_letter = all_students.filter(clazz__letter=class_letter)
        students_by_number_and_letter = students_by_number.filter(clazz__letter=class_letter)

        if class_number and class_letter:
            return students_by_number_and_letter
        else:
            if class_number:
                return students_by_number
            elif class_letter:
                return students_by_letter

        return all_students


class GradesList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = GradesSerializer
    queryset = Grade.objects.all()
    filter_backends = (GradeFilterBackend,)
    pagination_class = None


class GradesDetail(generics.ListCreateAPIView):
    permission_classes_by_action = {
        'get': (IsAuthenticated, IsValidUser),
        'post': (IsAuthenticated, IsTeacher, IsTeachersSubject)
    }
    serializer_class = GradesSerializer

    def get_permissions(self):
        return [
            permission()
            for permission
            in self.permission_classes_by_action[self.request.method.lower()]
        ]

    def get(self, request, *args, **kwargs):
        user = generics.get_object_or_404(User, id=kwargs['user_pk'])

        if IsStudent().has_permission(request, self):
            self.check_object_permissions(request, user)

        grades = Grade.objects.filter(
            subject__id=kwargs['subject_pk']
        ).filter(
            student__id=user.student.pk
        )

        serializer = self.serializer_class(grades, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        subject = generics.get_object_or_404(Subject, id=kwargs['subject_pk'])
        self.check_object_permissions(request, subject)

        user = generics.get_object_or_404(User, id=kwargs['user_pk'])

        context = {
            'request': request,
            'subject': subject,
            'student': user.student
        }

        serializer = self.serializer_class(context=context, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)

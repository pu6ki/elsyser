from rest_framework import permissions

from .models import Student, Teacher


ROLE_DEFAULT_MESSAGE = 'Only {}s are allowed to view and modify this content.'
AUTHOR_DEFAULT_MESSAGE = 'You should be the author of this content in order to modify it.'


class IsValidUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsStudent(permissions.BasePermission):
    message = ROLE_DEFAULT_MESSAGE.format('student')

    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists()


class IsTeacher(permissions.BasePermission):
    message = ROLE_DEFAULT_MESSAGE.format('teacher')

    def has_permission(self, request, view):
        return Teacher.objects.filter(user=request.user).exists()


class IsUserAuthor(permissions.BasePermission):
    message = AUTHOR_DEFAULT_MESSAGE

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsStudentAuthor(permissions.BasePermission):
    message = AUTHOR_DEFAULT_MESSAGE

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.student


class IsTeacherAuthor(permissions.BasePermission):
    message = AUTHOR_DEFAULT_MESSAGE

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.teacher


class IsTeachersSubject(permissions.BasePermission):
    message = 'You can modify content linked only with your subject.'

    def has_object_permission(self, request, view, obj):
        return obj == request.user.teacher.subject

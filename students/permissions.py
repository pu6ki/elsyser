from rest_framework import permissions

from .models import Student, Teacher


class IsValidUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists()


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return Teacher.objects.filter(user=request.user).exists()


class IsUserAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsStudentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.student


class IsTeacherAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.teacher


class IsTeachersSubject(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user.teacher.subject

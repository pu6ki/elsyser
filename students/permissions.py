from rest_framework import permissions

from .models import Student, Teacher


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists()


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return Teacher.objects.filter(user=request.user).exists()

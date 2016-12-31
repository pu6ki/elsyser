from rest_framework import permissions

from students.models import Student


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return Student.objects.filter(user=request.user).exists()


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Teachers').exists()

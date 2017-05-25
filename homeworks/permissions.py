from rest_framework import permissions


class HasOnlyOneSubmission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.submission_set.filter(student=request.user.student)


class IsValidStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user.student


class IsNotChecked(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return not obj.checked

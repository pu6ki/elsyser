from rest_framework import permissions


class HasOnlyOneSubmission(permissions.BasePermission):
    message = 'You can submit only one submission.'

    def has_object_permission(self, request, view, obj):
        return not obj.submission_set.filter(student=request.user.student)


class IsValidStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.student == request.user.student


class IsNotChecked(permissions.BasePermission):
    message = 'Submission is already checked.'

    def has_object_permission(self, request, view, obj):
        return not obj.checked

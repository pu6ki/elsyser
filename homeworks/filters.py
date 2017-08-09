from rest_framework import filters

from students.permissions import IsTeacher, IsStudent


class HomeworksFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if IsTeacher().has_permission(request, self):
            return queryset.filter(subject=request.user.teacher.subject)

        return queryset.filter(clazz=request.user.student.clazz)


class SubmissionsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if IsStudent().has_permission(request, self):
            return queryset.filter(student=request.user.student).first()

        return queryset.filter(checked=False)

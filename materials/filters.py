from rest_framework import filters

from students.permissions import IsTeacher


class MaterialListFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if IsTeacher().has_permission(request, self):
            return queryset.filter(subject=request.user.teacher.subject)

        return queryset.filter(class_number=request.user.student.clazz.number)

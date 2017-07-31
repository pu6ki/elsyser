from collections import defaultdict

from rest_framework import filters
from rest_framework.generics import get_object_or_404

from .models import Class


class GradeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(subject__id=view.kwargs['subject_pk']).order_by('-pk')


class StudentsListFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        clazz = get_object_or_404(
            Class,
            number=view.kwargs['class_number'],
            letter=view.kwargs['class_letter']
        )

        return queryset.filter(clazz=clazz)


class ClassNumberFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(number=view.kwargs['class_number'])

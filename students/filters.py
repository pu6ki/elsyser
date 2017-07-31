from rest_framework import filters


class GradeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(subject__id=view.kwargs['subject_pk']).order_by('-pk')

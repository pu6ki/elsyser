from rest_framework import filters


class GradeFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        class_letter = request.query_params.get('class_letter', '')
        class_number = request.query_params.get('class_number')

        queryset = queryset.filter(subject__id=view.kwargs['subject_pk']).order_by('-pk')

        if class_letter:
            queryset = queryset.filter(student__clazz__letter=class_letter)
        if class_number:
            queryset = queryset.filter(student__clazz__number=class_number)

        return queryset

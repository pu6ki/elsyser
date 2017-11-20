from datetime import datetime

from rest_framework import filters


class MeetupsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        only = request.query_params.get('only')
        now = datetime.now()

        if only == 'past':
            return queryset.filter(date__lte=now)
        elif only == 'upcoming':
            return queryset.filter(date__gte=now)

        return queryset

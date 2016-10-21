from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Class, Exam


class AllExamsView(ListView):
    model = Exam
    template_name = 'exams/list.html'
    context_object_name = 'exams'
    paginate_by = 5

    def get_queryset(self):
        return get_list_or_404(self.model)


class AllClassExamsView(AllExamsView):
    def get_queryset(self):
        return get_list_or_404(
            self.model,
            clazz__number=self.kwargs['class_number']
        )


class CertainClassExamsView(AllExamsView):
    def get_queryset(self):
        clazz = get_object_or_404(
            Class,
            number=self.kwargs['class_number'],
            title=self.kwargs['class_title']
        )

        return get_list_or_404(self.model, clazz=clazz)

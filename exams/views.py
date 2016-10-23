from datetime import datetime, timedelta

from django.views.generic import ListView

from .models import Exam, Class
from .serializers import ExamsSerializer


class ExamsList(ListView):

    model = Exam
    template_name = 'exams/list.html'
    context_object_name = 'exams'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(
            date__lte=datetime.now()+timedelta(days=5)
        )


class AllClassExamsList(ExamsList):

    def get_queryset(self):
        return self.model.objects.filter(
            date__lte=datetime.now()+timedelta(days=5),
            clazz__number=self.kwargs['class_number'],
        )


class CertainClassExamsList(ExamsList):

    def get_queryset(self):
        clazz = Class.objects.get(
            number=self.kwargs['class_number'],
            title=self.kwargs['class_title'],
        )

        return self.model.objects.filter(
            date__lte=datetime.now()+timedelta(days=5),
            clazz=clazz,
        )

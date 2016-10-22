from django.views.generic import ListView
from django.http import Http404

from datetime import datetime, timedelta

from .models import Exam, Class


class AllExamsView(ListView):
    model = Exam
    template_name = 'exams/list.html'
    context_object_name = 'exams'
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.filter(
            date__lte=datetime.now()+timedelta(days=5)
        )


class AllClassExamsView(AllExamsView):
    def get_queryset(self):
        return self.model.objects.filter(
            date__lte=datetime.now()+timedelta(days=5),
            clazz__number=self.kwargs['class_number']
        )


class CertainClassExamsView(AllExamsView):
    def get_queryset(self):
        clazz = Class.objects.get(
            number=self.kwargs['class_number'],
            title=self.kwargs['class_title']
        )

        return self.model.objects.filter(
            date__lte=datetime.now()+timedelta(days=5),
            clazz=clazz
        )

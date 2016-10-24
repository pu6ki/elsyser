from datetime import datetime, timedelta

from rest_framework import generics

from .models import Exam, Class
from .serializers import ExamsSerializer


class ExamsList(generics.ListCreateAPIView):

    queryset = Exam.objects.filter(date__lte=datetime.now()+timedelta(days=5))
    serializer_class = ExamsSerializer


class AllClassExamsList(generics.ListAPIView):

    serializer_class = ExamsSerializer

    def get_queryset(self):
        return Exam.objects.filter(
            date__lte=datetime.now()+timedelta(days=5),
            clazz__number=self.kwargs['class_number'],
        )


class CertainClassExamsList(AllClassExamsList):

    def get_queryset(self):
        clazz = Class.objects.get(
            number=self.kwargs['class_number'],
            title=self.kwargs['class_title'],
        )

        return Exam.objects.filter(
            date__lte=datetime.now()+timedelta(days=5),
            clazz=clazz,
)

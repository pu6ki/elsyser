from datetime import datetime, timedelta

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Exam, Class
from .serializers import ExamsSerializer


class ExamsList(generics.ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Exam.objects.filter(date__gte=datetime.now().date())
    serializer_class = ExamsSerializer


class AllClassExamsList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExamsSerializer

    def get_queryset(self):
        return Exam.objects.filter(
            date__gte=datetime.now().date(),
            clazz__number=self.kwargs['class_number'],
        )


class CertainClassExamsList(AllClassExamsList):

    def get_queryset(self):
        clazz = Class.objects.get(
            number=self.kwargs['class_number'],
            title=self.kwargs['class_title'],
        )

        return Exam.objects.filter(
            date__gte=datetime.now().date(),
            clazz=clazz,
)

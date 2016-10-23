from django.conf.urls import url

from .views import ExamsList, AllClassExamsList, CertainClassExamsList

app_name = 'exams'
urlpatterns = [
    url(
        r'^$',
        ExamsList.as_view(),
        name='get_exams'
    ),
    url(
        r'^(?P<class_number>8|9|1[0-2])/$',
        AllClassExamsList.as_view(),
        name='get_all_class_exams'
    ),
    url(
        r'^(?P<class_number>8|9|1[0-2])/(?P<class_title>A|B|V|G)/$',
        CertainClassExamsList.as_view(),
        name='get_certain_class_exams'
    ),
]

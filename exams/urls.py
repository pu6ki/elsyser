from django.conf.urls import url

from . import views

app_name = 'exams'
urlpatterns = [
    url(
        r'^$',
        views.all_exams_list,
        name='all-exams-list'
    ),
    url(
        r'^(?P<class_number>[0-9]+)/$',
        views.all_class_exams_list,
        name='all-class-exams-list'
    ),
    url(
        r'^(?P<class_number>[0-9]+)/(?P<class_title>[A-Z])/$',
        views.class_exam_list,
        name='class-exam-list'
    ),
]

from django.conf.urls import url

from . import views

app_name = 'exams'
# TODO: /exams/10/A/exam_id
urlpatterns = [
    url(r'^$', views.exams_list, name='exams-list'),
    url(r'^(?P<pk>[0-9]+)/$', views.ExamDetailView.as_view(), name='exam-detail'),
]

from django.conf.urls import url

from . import views

app_name = 'exams'
urlpatterns = [
    url(
        r'^$',
        views.AllExamsView.as_view(),
        name='all-exams-list'
    ),
    url(
        r'^(?P<class_number>[0-9]+)/$',
        views.AllClassExamsView.as_view(),
        name='all-class-exams-list'
    ),
    url(
        r'^(?P<class_number>[0-9]+)/(?P<class_title>[A-Z])/$',
        views.CertainClassExamsView.as_view(),
        name='certain-class-exam-list'
    ),
]

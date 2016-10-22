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
        r'^(?P<class_number>8|9|1[0-2])/$',
        views.AllClassExamsView.as_view(),
        name='all-class-exams-list'
    ),
    url(
        r'^(?P<class_number>8|9|1[0-2])/(?P<class_title>A|B|V|G)/$',
        views.CertainClassExamsView.as_view(),
        name='certain-class-exam-list'
    ),
]

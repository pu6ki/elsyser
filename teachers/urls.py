from django.conf.urls import url

from .views import AddExam, EditExam


app_name = 'teachers'
urlpatterns = [
    url(r'^add-exam/$', AddExam.as_view(), name='add-exam'),
    url(r'^edit-exam/(?P<pk>\d+)/$', EditExam.as_view(), name='edit-exam'),
]

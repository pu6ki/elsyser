from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('students.urls', namespace='students')),
    url(r'^', include('news.urls', namespace='news')),
    url(r'^', include('exams.urls', namespace='exams')),
    url(r'^', include('homeworks.urls', namespace='homeworks')),
    url(r'^', include('materials.urls', namespace='materials')),
]

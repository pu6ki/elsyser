from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('students.urls')),
    url(r'^', include('news.urls')),
    url(r'^', include('exams.urls')),
    url(r'^', include('homeworks.urls')),
    url(r'^', include('materials.urls')),
]

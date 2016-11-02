from django.conf.urls import url, include

urlpatterns = [
    url(r'', include('students.urls')),
    url(r'', include('teachers.urls')),
]

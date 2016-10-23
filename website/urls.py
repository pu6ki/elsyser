from django.conf.urls import url, include


app_name = 'website'
urlpatterns = [
    url(r'^exams/', include('exams.urls')),
]

from django.conf.urls import url, include

from .views import StudentRegistration, StudentProfile, ExamsList, NewsList


app_name = 'students'
urlpatterns = [
    url(r'^register/', StudentRegistration.as_view(), name='register'),
    url(r'^profile/', StudentProfile.as_view(), name='profile'),
    url(r'^exams/', ExamsList.as_view(), name='exams'),
    url(r'^news/', NewsList.as_view(), name='news'),
]

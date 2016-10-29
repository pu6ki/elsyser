from django.conf.urls import url, include
from django.contrib.auth.views import login, logout

from .views import StudentRegistration, StudentProfile, ExamsList


app_name = 'students'
urlpatterns = [
    url(r'^register/', StudentRegistration.as_view(), name='register'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^profile/', StudentProfile.as_view(), name='profile'),
    url(r'^exams/', ExamsList.as_view(), name='exams'),
]

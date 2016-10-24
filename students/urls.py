from django.conf.urls import url, include

from .views import StudentRegistration, StudentLogin, StudentProfile

app_name = 'students'
urlpatterns = [
    url(r'^register/', StudentRegistration.as_view(), name='register'),
    url(r'^login/', StudentLogin.as_view(), name='login'), # Under construction!!!
    url(r'^profile/', StudentProfile.as_view(), name='profile'),
]

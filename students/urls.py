from django.conf.urls import url, include

from .views import StudentRegistration

app_name = 'students'
urlpatterns = [
    url(r'^register/', StudentRegistration.as_view(), name='register'),
]

from django.conf.urls import url, include

from .views import UserRegistration

app_name = 'website'
urlpatterns = [
    url(r'^register/', UserRegistration.as_view(), name='register'),
    url(r'^exams/', include('exams.urls')),
]

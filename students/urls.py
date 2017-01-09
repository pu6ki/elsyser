from django.conf.urls import url, include

from rest_framework import routers

from students.views import (
    UserLogin, ProfileViewSet, StudentRegistration, SubjectsList
)


app_name = 'students'

router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^subjects/$', SubjectsList.as_view(), name='subjects-list'),
]

urlpatterns += router.urls

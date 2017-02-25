from django.conf.urls import url, include

from rest_framework import routers

from students.views import (
    UserLogin, ProfileViewSet, StudentRegistration, SubjectsList,
    GradesList, GradesDetail
)

app_name = 'students'

router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^subjects/$', SubjectsList.as_view(), name='subjects-list'),
    url(
        r'^grades/(?P<subject_pk>[0-9]+)/$',
        GradesList.as_view(),
        name='grades-list'
    ),
    url(
        r'^grades/(?P<subject_pk>[0-9]+)/(?P<student_pk>[0-9]+)/$',
        GradesDetail.as_view(),
        name='grades-detail'
    )
]

urlpatterns += router.urls

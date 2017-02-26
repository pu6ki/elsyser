from django.conf.urls import url, include

from rest_framework import routers

from students.views import (
    UserLogin, ProfileViewSet, StudentRegistration, SubjectsList,
    GradesList, GradesDetail,
    StudentsList
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
        r'^grades/(?P<subject_pk>[0-9]+)/(?P<user_pk>[0-9]+)/$',
        GradesDetail.as_view(),
        name='grades-detail'
    ),
    url(
        r'^students/(?P<class_number>[8]|[9]|1[0-2])/(?P<class_letter>[A]|[B]|[V]|[G])/$',
        StudentsList.as_view(),
        name='students-list'
    )
]

urlpatterns += router.urls

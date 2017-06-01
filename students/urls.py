from django.conf.urls import url
from rest_framework import routers

from .views import (
    UserLogin, ProfileViewSet, StudentRegistration,
    SubjectsList,
    ClassesList, ClassesNumberList,
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
    url(r'^classes/$', ClassesList.as_view(), name='classes-list'),
    url(
        r'^classes/(?P<class_number>[8]|[9]|1[0-2])/$',
        ClassesNumberList.as_view(),
        name='classes-number-list'
    ),
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
        r'^students/(?P<class_number>[8]|[9]|1[0-2])/(?P<class_letter>[A-Z])/$',
        StudentsList.as_view(),
        name='students-list'
    ),
]

urlpatterns += router.urls

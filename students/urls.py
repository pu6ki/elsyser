from django.conf.urls import url
from rest_framework import routers

from .views import (
    StudentRegistration, AccountActivation, ChangePassword, UserLogin,
    ProfileViewSet,
    SubjectsList,
    ClassesList,
    StudentsList,
    GradesList, GradesDetail
)


app_name = 'students'

router = routers.SimpleRouter()
router.register(r'profile', ProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        AccountActivation.as_view(),
        name='activation'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^change-password/$', ChangePassword.as_view(), name='change-password'),
    url(r'^subjects/$', SubjectsList.as_view(), name='subjects-list'),
    url(r'^classes/$', ClassesList.as_view(), name='classes-list'),
    url(r'^students/$', StudentsList.as_view(), name='students-list'),
    url(r'^grades/(?P<subject_pk>[0-9]+)/$', GradesList.as_view(), name='grades-list'),
    url(r'^grades/(?P<subject_pk>[0-9]+)/(?P<user_pk>[0-9]+)/$',
        GradesDetail.as_view(),
        name='grades-detail')
]

urlpatterns += router.urls

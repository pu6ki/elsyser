from django.conf.urls import url

from rest_framework import routers
from djoser.views import SetPasswordView, PasswordResetView, PasswordResetConfirmView

from . import views


app_name = 'students'

router = routers.SimpleRouter()
router.register(r'profile', views.ProfileViewSet, base_name='profile')

urlpatterns = [
    url(r'^register/$', views.StudentRegistration.as_view(), name='register'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        views.AccountActivation.as_view(),
        name='activation'),
    url(r'^password/change/$', SetPasswordView.as_view(), name='change_password'),
    url(r'^password/reset/$', PasswordResetView.as_view(), name='password_reset'),
    url(r'^password/reset/confirm/$',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    url(r'^login/$', views.UserLogin.as_view(), name='login'),
    url(r'^subjects/$', views.SubjectsList.as_view(), name='subjects_list'),
    url(r'^classes/$', views.ClassesList.as_view(), name='classes_list'),
    url(r'^students/$', views.StudentsList.as_view(), name='students_list'),
    url(r'^grades/(?P<subject_pk>[0-9]+)/$', views.GradesList.as_view(), name='grades_list'),
    url(r'^grades/(?P<subject_pk>[0-9]+)/(?P<user_pk>[0-9]+)/$',
        views.GradesDetail.as_view(),
        name='grades_detail')
]

urlpatterns += router.urls

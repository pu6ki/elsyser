from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from .views import (
    StudentRegistration,
    UserLogin,
    StudentProfile,
    ExamsList,
    NewsViewSet,
    HomeworksList
)


router = routers.SimpleRouter()
router.register(r'news', NewsViewSet, base_name='news')

app_name = 'students'
urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^profile/$', StudentProfile.as_view(), name='profile'),
    url(r'^exams/$', ExamsList.as_view(), name='exams'),
    url(r'^homeworks/$', HomeworksList.as_view(), name='homeworks')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls

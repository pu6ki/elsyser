from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from .views import (
    StudentRegistration,
    UserLogin,
    StudentProfile,
    ExamsList,
    NewsList,
    NewsDetail
)

app_name = 'students'
urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^profile/$', StudentProfile.as_view(), name='profile'),
    url(r'^exams/$', ExamsList.as_view(), name='exams'),
    url(r'^news/$', NewsList.as_view(), name='news-list'),
    url(r'^news/(?P<pk>[0-9]+)/$', NewsDetail.as_view(), name='news-detail'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_nested import routers

from .views import (
    StudentRegistration,
    UserLogin,
    StudentProfile,
    ExamsList,
    NewsViewSet,
    CommentsViewSet,
    HomeworksList
)


news_router = routers.SimpleRouter()
news_router.register(r'news', NewsViewSet, base_name='news')

comments_router = routers.NestedSimpleRouter(news_router, r'news', lookup='news')
comments_router.register(r'comments', CommentsViewSet, base_name='comments')

app_name = 'students'
urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^profile/$', StudentProfile.as_view(), name='profile'),
    url(r'^exams/$', ExamsList.as_view(), name='exams'),
    url(r'^homeworks/$', HomeworksList.as_view(), name='homeworks')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += news_router.urls
urlpatterns += comments_router.urls

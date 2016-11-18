from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_nested import routers

from .views import (
    StudentRegistration, UserLogin, StudentProfile,
    ExamsViewSet,
    NewsViewSet, CommentsViewSet,
    HomeworksViewSet
)


router = routers.SimpleRouter()
router.register(r'news', NewsViewSet, base_name='news')
router.register(r'exams', ExamsViewSet, base_name='exams')
router.register(r'homeworks', HomeworksViewSet, base_name='homeworks')

comments_router = routers.NestedSimpleRouter(router, r'news', lookup='news')
comments_router.register(r'comments', CommentsViewSet, base_name='comments')

app_name = 'students'
urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^profile/$', StudentProfile.as_view(), name='profile'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += router.urls
urlpatterns += comments_router.urls

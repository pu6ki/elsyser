from django.conf.urls import url, include

from rest_framework_nested import routers

from .views import (
    UserLogin, UserProfile,
    StudentRegistration,
    SubjectsList,
    ExamsViewSet,
    NewsViewSet, CommentsViewSet,
    HomeworksViewSet,
    MaterialsListViewSet, NestedMaterialsViewSet
)

router = routers.SimpleRouter()

router.register(r'news', NewsViewSet, base_name='news')
router.register(r'exams', ExamsViewSet, base_name='exams')
router.register(r'homeworks', HomeworksViewSet, base_name='homeworks')
router.register(r'materials', MaterialsListViewSet, base_name='materials')
router.register(r'materials/(?P<subject_pk>[0-9]+)', NestedMaterialsViewSet, base_name='nested-materials')

news_comments_router = routers.NestedSimpleRouter(
    router, r'news', lookup='news'
)
news_comments_router.register(
    r'comments', CommentsViewSet, base_name='news-comments'
)

app_name = 'students'
urlpatterns = [
    url(r'^register/$', StudentRegistration.as_view(), name='register'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^profile/$', UserProfile.as_view(), name='profile'),
    url(r'^subjects/$', SubjectsList.as_view(), name='subjects-list'),
]

urlpatterns += router.urls
urlpatterns += news_comments_router.urls

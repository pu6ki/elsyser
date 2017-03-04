from django.conf.urls import url, include

from rest_framework_nested import routers

from news.views import (
    NewsStudentsViewSet,
    NewsTeachersClassNumberList, NewsTeachersViewSet,
    CommentsViewSet
)

app_name = 'news'

students_router = routers.SimpleRouter()
students_router.register(
    r'news/students',
    NewsStudentsViewSet,
    base_name='students_news'
)

teachers_router = routers.SimpleRouter()
teachers_router.register(
    r'news/teachers/(?P<class_number>[8]|[9]|1[0-2])/(?P<class_letter>[A-Z])',
    NewsTeachersViewSet,
    base_name='teachers_news'
)

students_comments_router = routers.NestedSimpleRouter(
    students_router, r'news/students', lookup='students_news'
)
students_comments_router.register(
    r'comments', CommentsViewSet, base_name='students_news_comments'
)

teachers_comments_router = routers.NestedSimpleRouter(
    teachers_router,
    r'news/teachers/(?P<class_number>[8]|[9]|1[0-2])/(?P<class_letter>[A-Z])',
    lookup='teachers_news'
)
teachers_comments_router.register(
    r'comments', CommentsViewSet, base_name='teachers_news_comments'
)

urlpatterns = [
    url(
        r'^news/teachers/(?P<class_number>[8]|[9]|1[0-2])/$',
        NewsTeachersClassNumberList.as_view(),
        name='teachers_class_number_list'
    )
]

urlpatterns += students_router.urls
urlpatterns += teachers_router.urls
urlpatterns += students_comments_router.urls
urlpatterns += teachers_comments_router.urls

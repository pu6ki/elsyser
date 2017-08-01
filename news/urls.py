from django.conf.urls import url

from rest_framework_nested import routers

from .views import (
    NewsStudentsViewSet,
    NewsTeachersList, NewsTeachersClassNumberList, NewsTeachersViewSet,
    CommentsViewSet
)


app_name = 'news'

students_url_pattern = r'news/students'
teachers_default_url_pattern = r'news/teachers'
teachers_detail_url_pattern = r'(?P<class_number>[8]|[9]|1[0-2])/(?P<class_letter>[A-Z])'
teachers_url_pattern = r'{default_pattern}/{detail_pattern}'.format(
    default_pattern=teachers_default_url_pattern,
    detail_pattern=teachers_detail_url_pattern
)

students_router = routers.SimpleRouter()
students_router.register(students_url_pattern, NewsStudentsViewSet, base_name='studentsNews')

teachers_router = routers.SimpleRouter()
teachers_router.register(teachers_url_pattern, NewsTeachersViewSet, base_name='teachersNews')

students_comments_router = routers.NestedSimpleRouter(
    students_router, students_url_pattern, lookup='studentsNews'
)
students_comments_router.register(r'comments', CommentsViewSet, base_name='studentsNews-comments')

teachers_comments_router = routers.NestedSimpleRouter(
    teachers_router, teachers_url_pattern, lookup='teachersNews'
)
teachers_comments_router.register(r'comments', CommentsViewSet, base_name='teachersNews-comments')

urlpatterns = [
    url(r'^news/teachers/$', NewsTeachersList.as_view(), name='teachers-news-list'),
    url(
        r'^news/teachers/(?P<class_number>[8]|[9]|1[0-2])/$',
        NewsTeachersClassNumberList.as_view(),
        name='teachers-class-number-list'
    )
]

urlpatterns += students_router.urls
urlpatterns += teachers_router.urls
urlpatterns += students_comments_router.urls
urlpatterns += teachers_comments_router.urls

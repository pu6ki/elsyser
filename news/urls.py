from rest_framework_nested import routers

from news.views import NewsViewSet, CommentsViewSet


router = routers.SimpleRouter()
router.register(r'news', NewsViewSet, base_name='news')

news_comments_router = routers.NestedSimpleRouter(
    router, r'news', lookup='news'
)
news_comments_router.register(
    r'comments', CommentsViewSet, base_name='news-comments'
)

urlpatterns = router.urls
urlpatterns += news_comments_router.urls

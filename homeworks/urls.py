from rest_framework_nested import routers

from homeworks.views import HomeworksViewSet, SubmissionsViewSet

app_name = 'homeworks'

router = routers.SimpleRouter()
router.register(r'homeworks', HomeworksViewSet, base_name='homeworks')

homework_submissions_router = routers.NestedSimpleRouter(
    router, r'homeworks', lookup='homeworks'
)
homework_submissions_router.register(
    r'submissions', SubmissionsViewSet, base_name='submissions'
)

urlpatterns = router.urls
urlpatterns += homework_submissions_router.urls

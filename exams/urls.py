from rest_framework import routers

from exams.views import ExamsViewSet


router = routers.SimpleRouter()
router.register(r'exams', ExamsViewSet, base_name='exams')

urlpatterns = router.urls

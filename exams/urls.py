from rest_framework import routers

from .views import ExamsViewSet


app_name = 'exams'

router = routers.SimpleRouter()
router.register(r'exams', ExamsViewSet, base_name='exams')

urlpatterns = router.urls

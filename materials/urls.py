from rest_framework import routers

from .views import MaterialsListViewSet, NestedMaterialsViewSet


app_name = 'materials'

router = routers.SimpleRouter()

router.register(r'materials', MaterialsListViewSet, base_name='materials')
router.register(
    r'materials/(?P<subject_pk>[0-9]+)', NestedMaterialsViewSet, base_name='nested-materials'
)

urlpatterns = router.urls

from rest_framework_nested import routers

from materials.views import MaterialsListViewSet, NestedMaterialsViewSet

router = routers.SimpleRouter()

router.register(r'materials', MaterialsListViewSet, base_name='materials')
router.register(
    r'materials/(?P<subject_pk>[0-9]+)',
    NestedMaterialsViewSet,
    base_name='nested-materials'
)

urlpatterns = router.urls

from django.conf.urls import url

from rest_framework_nested import routers

from .views import MeetupsViewSet, TalksViewSet


app_name = 'talks'

meetups_router = routers.SimpleRouter()
meetups_router.register(r'meetups', MeetupsViewSet, base_name='meetups')

talks_router = routers.NestedSimpleRouter(
    parent_router=meetups_router,
    parent_prefix=r'meetups',
    lookup='meetups'
)
talks_router.register(r'talks', TalksViewSet, base_name='talks')

urlpatterns = meetups_router.urls
urlpatterns += talks_router.urls

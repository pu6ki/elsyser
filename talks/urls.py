from django.conf.urls import url

from rest_framework import routers

from .views import TalksViewSet, VoteTalk


app_name = 'talks'

router = routers.SimpleRouter()
router.register('talks', TalksViewSet, base_name='talks')

urlpatterns = [
    url(r'^talks/(?P<pk>\d+)/(?P<action>upvote|downvote)/$', VoteTalk.as_view(), name='vote-talk'),
]
urlpatterns += router.urls

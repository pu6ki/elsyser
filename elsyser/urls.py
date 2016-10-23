from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'', include('website.urls')),
    url(r'^exams/', include('exams.urls')),
    url(r'', include('django.contrib.auth.urls')),
]

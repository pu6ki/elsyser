from django.conf.urls import url, include

from .views import home, register, profile


app_name = 'website'
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^register/$', register, name='register'),
    url(r'^accounts/profile/$', profile, name='profile'),

]

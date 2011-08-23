from django.conf.urls.defaults import *
import hhg_app
import like

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<songid>\d+)/$', 'like.views.like_song', name='like-song'),
    url(r'^(?P<songid>\d+)/un/$', 'like.views.unlike_song', name='unlike-song'),
)


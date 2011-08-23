from django.conf.urls.defaults import *
import hhg_app
import search
import upload
import like
import avatar

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    url(r'^$', 'hhg_app.views.hhg_stage'),
    #url(r'^like/', include('like.urls')),
    url(r'^staging/$','hhg_app.views.hhg_stage'),
    url(r'^backend/$',include('hhg_app.urls')),
    url(r'^getdata/$','hhg_app.views.getdata'),
    url(r'^gettwitter/$','hhg_app.views.get_twitter_widget'),
    url(r'^getsimilars/$','hhg_app.views.getsimilars'),
    url(r'^getregisterform/$','hhg_app.views.getregisterform'),
    url(r'^upload/', 'hhg_app.views.upload'),
    url(r'^secret/downloads/','hhg_app.views.secret'),
    url(r'^play/(?P<alias>\w+)/$','hhg_app.views.playlist'),
    url(r'^play/(?P<alias>\w+)/getnext/(?P<id>\d+)/$','hhg_app.views.playlistnext'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^static/(.*)$', 'django.views.static.serve', kwargs={'document_root': '/home/hiphopgoblin/webapps/django/hhg/static/'}),
    url(r'^random/$', 'hhg_app.views.random'),
    url(r'^hot/(?P<songid>\d+)/$', 'hhg_app.views.hot'),
    url(r'^(?P<songid>\d+)/$', 'hhg_app.views.track'),
    url(r'^scrape/$', 'hhg_app.views.getsongs'),
    url(r'^clean/$', 'hhg_app.views.clean'),
    url(r'^like/(?P<id>\d+)/$', 'hhg_app.views.like'),
    url(r'^unlike/(?P<id>\d+)/$', 'hhg_app.views.unlike'),
    url(r'^login/', 'hhg_app.views.login'),
    url(r'^edit/$', 'hhg_app.views.edit'),
    url(r'^logout/', 'hhg_app.views.logout'),
    url(r'^register/', 'hhg_app.views.register'),
    url(r'^search/$', 'hhg_app.views.search'),
    url(r'^song_info/(?P<id>\d+)/$','hhg_app.views.song_info'),
    url(r'^comment/(?P<id>\d+)/$','hhg_app.views.comment'),
    url(r'^get_likes/$','hhg_app.views.get_likes'),
    url(r'^avatar/', include('avatar.urls')),
    (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': '/static/skin/favicon.ico'}),
)


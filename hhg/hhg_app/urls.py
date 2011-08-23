from django.conf.urls.defaults import *
import hhg_app.views as views

urlpatterns = patterns('',
    url(r'', views.hhg),
    url(r'^list/$', views.list),
)

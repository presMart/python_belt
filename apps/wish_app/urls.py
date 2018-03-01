from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dash$', views.dash),
    url(r'^dash/info/(?P<wish_id>\d+)$', views.info),
    url(r'^add$', views.add),
    url(r'^new$', views.new),
    url(r'^want/(?P<id>\d+)$', views.want),
    url(r'^unwant/(?P<id>\d+)$', views.unwant),
    url(r'^forget/(?P<id>\d+)$', views.forget),
]
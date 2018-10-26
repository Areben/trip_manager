from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^logout$', views.logout),
	url(r'^addtrip$', views.addtrip),
	url(r'^register$', views.register),
	url(r'^createplan$', views.createplan),
	url(r'^join/(?P<trip_id>\d+)$', views.join),
	url(r'^cancel/(?P<trip_id>\d+)$', views.cancel),
	url(r'^delete/(?P<trip_id>\d+)$', views.delete),
	url(r'^travels/(?P<user_id>\d+)$', views.travels),
	url(r'^viewtrip/(?P<trip_id>\d+)$', views.viewtrip),
]

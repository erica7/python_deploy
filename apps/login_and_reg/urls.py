from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.redirect_to_main),
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
    url(r'^quotes/create$', views.create),
    url(r'^quotes/(?P<id>\d+)/favorite$', views.favorite),
    url(r'^quotes/(?P<id>\d+)/remove_favorite$', views.remove_favorite),
    url(r'^users/(?P<id>\d+)$', views.users_page),
]
